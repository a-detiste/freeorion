# from __future__ import annotations

import freeOrionAIInterface as fo
from copy import copy
from logging import debug, error
from typing import Optional, Set, Union

import PlanetUtilsAI
from AIDependencies import Tags
from aistate_interface import get_aistate
from buildings import BuildingType
from common.fo_typing import PlanetId, SpeciesName
from EnumsAI import FocusType, PriorityType
from freeorion_tools import assertion_fails, get_species_tag_value
from freeorion_tools.caching import cache_for_current_turn
from turn_state import get_empire_planets_by_species

propaganda = "PLC_PROPAGANDA"
algo_research = "PLC_ALGORITHMIC_RESEARCH"
liberty = "PLC_LIBERTY"
diversity = "PLC_DIVERSITY"
artisans = "PLC_ARTISAN_WORKSHOPS"
industrialism = "PLC_INDUSTRIALISM"
technocracy = "PLC_TECHNOCRACY"
centralization = "PLC_CENTRALIZATION"
bureaucracy = "PLC_BUREAUCRACY"
infra1 = "PLC_PLANETARY_INFRA"
infra2 = "PLC_SYSTEM_INFRA"
infra3 = "PLC_INTERSTELLAR_INFRA"


class _EmpireOutput:
    def __init__(self):
        self.industry = 0.0
        self.research = 0.0
        self.influence = 0.0
        self.population_stability = 0.0
        self.stability_scaling = 0.75

    def __str__(self):
        return "pp=%.1f, rp=%.1f, ip=%.1f, population_stabililty=%d" % (
            self.industry,
            self.research,
            self.influence,
            self.population_stability,
        )

    def is_better_than(self, other, cost_for_other: float) -> bool:  # other: _EmpireOutput,
        """Return true if this is better than changing to other at given IP cost."""
        aistate = get_aistate()
        delta_pp = (self.industry - other.industry) * aistate.get_priority(PriorityType.RESOURCE_PRODUCTION)
        delta_rp = (self.research - other.research) * aistate.get_priority(PriorityType.RESOURCE_RESEARCH)
        delta_ip = (self.influence - other.influence) * aistate.get_priority(PriorityType.RESOURCE_INFLUENCE)
        delta_stability = self.population_stability - other.population_stability
        # delta is per round, adoption cost is a one-time cost
        cost = cost_for_other * aistate.get_priority(PriorityType.RESOURCE_INFLUENCE) / 10
        result = delta_pp + delta_rp + delta_ip + delta_stability + cost > 0
        debug(f"is_better_than: {delta_pp} + {delta_rp} + {delta_ip} + {delta_stability} + {cost} > 0 => {result}")
        return result

    def add_planet(self, planet: fo.planet) -> None:
        """Add output of the given planet to this object."""
        self.industry += planet.currentMeterValue(fo.meterType.targetIndustry)
        self.research += planet.currentMeterValue(fo.meterType.targetResearch)
        self.influence += planet.currentMeterValue(fo.meterType.targetInfluence)
        current_population = planet.currentMeterValue(fo.meterType.population)
        target_population = planet.currentMeterValue(fo.meterType.targetPopulation)
        # current is what counts now, but look a little ahead
        population = (3 * current_population + target_population) / 4
        # no bonuses above 20
        stability = min(planet.currentMeterValue(fo.meterType.targetHappiness), 20)
        if stability < -1:
            # increase both for the risk of losing the colony
            population += 1
            stability -= 1
        elif stability >= 10:
            # 10 give a lot of bonuses, increases above 10 are less important
            stability = 11 + (stability - 10) / 2
        self.population_stability += population * stability * self.stability_scaling


class PolicyManager:
    """Policy Manager for one round"""

    def __init__(self, status_only: bool = False):
        self._empire = fo.getEmpire()
        self._universe = fo.getUniverse()
        self._aistate = get_aistate()
        # resourceAvailable includes this turns production, but that is wrong for influence
        self._ip = self._empire.resourceAvailable(fo.resourceType.influence) - self._get_infl_prod()
        self._adopted = set(self._empire.adoptedPolicies)
        # When we continue a game in which we just adopted a policy, game state shows the policy as adopted,
        # but IP still unspent. Correct it here, then calculate anew whether we want to adopt it.
        if not status_only:
            for entry in self._empire.turnsPoliciesAdopted:
                if entry.data() == fo.currentTurn():
                    debug(f"reverting saved adopt {entry.key()}")
                    fo.issueDeadoptPolicyOrder(entry.key())
                    self._adopted.remove(entry.key())
        self._originally_adopted = copy(self._adopted)
        empire_owned_planet_ids = PlanetUtilsAI.get_owned_planets_by_empire()
        self._populated_planet_ids = PlanetUtilsAI.get_populated_planet_ids(empire_owned_planet_ids)
        self._num_populated = len(self._populated_planet_ids)
        self._num_outposts = len(empire_owned_planet_ids) - self._num_populated
        self._max_turn_bureaucracy = self._calculate_max_turn_bureaucracy()
        self._centralization_cost = fo.getPolicy(centralization).adoptionCost()
        self._bureaucracy_cost = fo.getPolicy(bureaucracy).adoptionCost()
        self._wanted_ip = self._wanted_for_bureaucracy()
        self._adoptable = self._get_adoptable()

    # Policies that may use IP "reserved" by wanted_ip.
    # The first two get IP specially reserved for them in the constructor.
    # If we are low on IP, adopting something that helps as gain IP should be worth it.
    # Technocracy and industrialism are important overall.
    _prioritised_policies = (bureaucracy, centralization, propaganda, artisans, technocracy, industrialism)

    def generate_orders(self) -> None:
        """The main task of the class, called once every turn by FreeOrionAI."""
        debug(
            "Start turn %d IP: %.2f + %.2f, adoptable: %s, adopted: %s",
            fo.currentTurn(),
            self._ip,
            self._get_infl_prod(),
            self._adoptable,
            self._adopted,
        )
        self._process_social()
        self._process_infrastructure()
        # TBD: military policies
        # we need the extra slots first
        if infra1 in self._adopted:
            self._process_bureaucracy()
            self._techno_or_industry()
        new_production = self._get_infl_prod(True)
        debug("End of turn IP: %.2f (wanted %.2f) + %.2f", self._ip, self._wanted_ip, new_production)
        self._determine_influence_priority(new_production)

    def _process_social(self) -> None:
        """
        Process social policies.
        So far we use propaganda, liberty, diversity, artisan workshops and algo. research.
        Propaganda is activated in turn 1 and usually replaced by liberty in 7.
        Since liberty affects so many other things, we check it first, then simply rate all others and
        try to adopt the best possible ones for the slots we have.
        """
        self._process_liberty()
        adopted = []
        may_adopt = []
        for policy in (propaganda, algo_research, diversity, artisans):
            rating = self._rate_policy(policy)
            cost = fo.getPolicy(policy).adoptionCost()
            if policy in self._adopted:
                if rating < 0:
                    self._deadopt(policy)
                else:
                    adopted.append((rating, policy))
            elif rating > 6:
                may_adopt.append((rating, policy, cost))
        if may_adopt:
            adopted.sort()
            may_adopt.sort()
            # Policies do not change too often, one per turn should do
            new_rating, new_policy, new_cost = may_adopt.pop()
            debug(f"_process_social: best new={new_policy}, rating={new_rating}, cost={new_cost}")
            if self._empire.emptyPolicySlots["SOCIAL_CATEGORY"]:
                if new_rating > new_cost / 3:
                    self._we_want(new_policy, new_cost)
            elif adopted:
                old_rating, old_policy = adopted.pop(0)
                debug(f"_process_social: lowest adopted={old_policy}, rating={old_rating}")
                if new_rating - old_rating > new_cost / 3:
                    self._we_want(new_policy, new_cost, old_policy)

    def _we_want(self, name: str, cost: float, replace: Optional[str] = None) -> None:
        if name not in self._empire.availablePolicies:
            unlocker = self._unlocked_by(name)
            if not assertion_fails(unlocker, f"_we_want: we can neither adopt nor unlock {name} yet"):
                debug(f"Trying to adopt {unlocker} to unlock {name}")
                self._we_want(unlocker, fo.getPolicy(unlocker).adoptionCost())
            return
        if self._can_adopt(name, replace):
            if replace:
                self._deadopt(replace)
            self._adopt(name)
        else:
            # We seem to have insufficient IP. Add cost to wanted_ip, to raise the influence priority
            self._wanted_ip += cost
            debug(f"Adopting {name} failed due to insufficient IP, adding {cost} to wanted_ip")

    @staticmethod
    def _unlocked_by(name: str) -> Optional[str]:
        """Returns another policy that unlocks the given policy, if any."""
        # Some day we should get that information from the server.
        # So far only one case.
        if name == artisans:
            return diversity
        return None

    @cache_for_current_turn
    def _rate_policy(self, name: str) -> float:
        """Gives a rough value of a policy."""
        if name == propaganda:
            return 20 + self._rate_opinion(name)
        if name == algo_research:
            return self._rate_algo_research()
        if name == diversity:
            return self._rate_diversity()
        if name == artisans:
            return self._rate_artisans()
        raise (ValueError(f"_rate_policy {name} not yet supported"))

    @staticmethod
    def _rate_opinion(name: str) -> float:
        """Return a rating value for the empire's planet opinion on a policy"""
        opinion = PlanetUtilsAI.get_planet_opinion(name)
        return 1.5 * (len(opinion.likes) - len(opinion.dislikes) * PlanetUtilsAI.dislike_factor())

    def _rate_algo_research(self) -> float:
        """Rate algorithmic research"""
        # First should do, but things may change. Liberty is more important!
        if fo.currentTurn() <= 10 or algo_research not in self._empire.availablePolicies:
            return 0.0
        # At 20 there are typically no planets with research focus
        # TBD: check how many planet have research focus or use meter_update?
        base_value = max(0, self._aistate.get_priority(PriorityType.RESOURCE_RESEARCH) - 20)
        rating = base_value + self._rate_opinion(algo_research)
        debug(f"_rate_algo_research: rating={rating}")
        return rating

    def _process_liberty(self) -> None:
        """
        Adopt or deadopt liberty, may replace another social policy.
        Liberty is available very early, but to help setting up basic policies we keep propaganda at least
        until we have infra1. Getting a second slot before that should be nearly impossible.
        Centralization is always kept only for one turn and if population has a strong opinion on it,
        stability calculation may be extremely different from normal turns, leading to a change that would
        possibly be reverted next turn, so we skip processing liberty while centralization is adopted.
        """
        could_replace = {propaganda, algo_research, diversity, artisans} & self._adopted
        if (
            infra1 in self._adopted
            and centralization not in self._adopted
            and (liberty in self._adopted or self._can_adopt(liberty, could_replace))
        ):
            adoption_cost = fo.getPolicy(liberty).adoptionCost()
            # liberty will generally make species less happy, but generates research
            debug("Evaluating liberty, first without change:")
            current_output = self._calculate_empire_output()
            if liberty in self._adopted:
                self._deadopt(liberty)
                without_liberty = self._calculate_empire_output()
                if current_output.is_better_than(without_liberty, 0):
                    self._universe.updateMeterEstimates(self._populated_planet_ids)
                    self._adopt(liberty)
            elif self._can_adopt(liberty):
                self._adopt(liberty)
                with_liberty = self._calculate_empire_output()
                if current_output.is_better_than(with_liberty, adoption_cost):
                    self._universe.updateMeterEstimates(self._populated_planet_ids)
                    self._deadopt(liberty)
            else:
                # Can only adopt it by replacing something. Note that we ignore the other replaced policies rating
                # here, since its effect is also evaluated by _calculate_empire_output.
                self._deadopt_one_of(could_replace)
                self._adopt(liberty)
                with_liberty = self._calculate_empire_output()
                if current_output.is_better_than(with_liberty, adoption_cost):
                    self._universe.updateMeterEstimates(self._populated_planet_ids)
                    self._deadopt(liberty)
                    self._readopt_selected_one()

    def _calculate_empire_output(self) -> _EmpireOutput:
        """Update empire meters, then calculate an estimation of the expected empire output."""
        # TBD: here we could use the stability-adapted update, that would be much better than trying
        # to rate the stability effects again production effects.
        self._universe.updateMeterEstimates(self._populated_planet_ids)
        result = _EmpireOutput()
        for pid in self._populated_planet_ids:
            result.add_planet(self._universe.getPlanet(pid))
        debug(f"Empire output: {result}")
        return result

    def _rate_diversity(self) -> float:
        """Rate diversity."""
        if diversity not in self._empire.availablePolicies:
            return 0.0
        # diversity affects stability, but also gives a bonus to research-focused planets and a little influence,
        diversity_value = len(get_empire_planets_by_species()) - fo.getNamedValue("PLC_DIVERSITY_THRESHOLD")
        diversity_scaling = fo.getNamedValue("PLC_DIVERSITY_SCALING")
        # Research bonus goes to research-focused planets only. With priority there are usually none.
        research_priority = self._aistate.get_priority(PriorityType.RESOURCE_RESEARCH)
        research_bonus = max(0, research_priority - 20)
        # + 4 for global influence
        global_influence_bonus = 4
        rating = self._rate_opinion(diversity) + diversity_scaling * diversity_value * (
            self._num_populated + global_influence_bonus + research_bonus
        )
        debug(
            f"_rate_diversity: rating={rating}. diversity_value={diversity_value}, "
            f"research priority={research_priority}"
        )
        return rating

    def _rate_artisans(self) -> float:
        """Rate artisan workshops."""
        # Diversity unlocks artisans, so if we have diversity, we could unlock artisans
        if diversity not in self._empire.availablePolicies:
            return 0.0
        # TBD: could use _calculate_empire_output, but we'd still have to check the species, since artistic
        # species may not be switched to influence.
        rating = 0.0
        artists = []
        for species_name, planets in get_empire_planets_by_species().items():
            species = fo.getSpecies(species_name)
            if Tags.ARTISTIC in species.tags:
                artists.append(species_name)
                for pid in planets:
                    rating += self._rate_artisan_planet(pid, species_name)
        rating += self._rate_opinion(artisans)
        debug(f"_rate_artisans: {rating}, artists: {artists}")
        return rating

    def _rate_artisan_planet(self, pid: PlanetId, species_name: SpeciesName) -> float:
        focus_bonus = fo.getNamedValue("ARTISANS_INFLUENCE_FLAT_FOCUS")
        focus_minimum = fo.getNamedValue("ARTISANS_MIN_STABILITY_FOCUS")
        species_focus_bonus = focus_bonus * get_species_tag_value(species_name, Tags.INFLUENCE)
        planet = self._universe.getPlanet(pid)
        stability = planet.currentMeterValue(fo.meterType.targetHappiness)
        # First check whether the planet would currently get the focus bonus.
        if planet.focus == FocusType.FOCUS_INFLUENCE:
            return 3 * species_focus_bonus if stability >= focus_minimum else 0.0

        # Planet does not have influence focus...
        # Check for the non-focus bonus. Since we would get this "for free", rate it higher
        non_focus_bonus = fo.getNamedValue("ARTISANS_INFLUENCE_FLAT_NO_FOCUS")
        non_focus_minimum = fo.getNamedValue("ARTISANS_MIN_STABILITY_NO_FOCUS")
        rating = 0.0
        if stability >= non_focus_minimum:
            rating += 4 * non_focus_bonus
        # Check whether this planet would get the focus bonus, if we'd switch it to influence.
        if PlanetUtilsAI.stability_with_focus(planet, FocusType.FOCUS_INFLUENCE) >= focus_minimum:
            rating += species_focus_bonus
        return rating

    def _process_infrastructure(self) -> None:
        """Handle infrastructure policies."""
        if infra1 in self._adoptable:
            self._adopt(infra1)
        # TBD infra2 / 3, then use the additional slot

    def _process_bureaucracy(self) -> None:
        """Handle adoption and regular re-adoption of bureaucracy and its prerequisite centralization."""
        if bureaucracy in self._adopted:
            if fo.currentTurn() >= self._empire.turnsPoliciesAdopted[bureaucracy] + self._max_turn_bureaucracy:
                self._deadopt(bureaucracy)
                self._try_adopt_centralization()
        else:
            self._try_adopt_bureaucracy()
        # We try not to adopt it when we cannot replace it, but enemy action may
        # make the best plans fails. Keeping it will usually cost too much influence.
        self._maybe_deadopt_centralization()

    def _try_adopt_centralization(self) -> None:
        """Try to adopt centralization as a prerequisite for bureaucracy.
        So far we only want actually adopt it if we can adopt bureaucracy next turn."""
        if centralization not in self._adoptable:
            return
        if self._centralization_cost + self._bureaucracy_cost > self._ip + self._get_infl_prod():
            return
        self._adopt(centralization)
        # Adopting centralization usually lowers IP production, so use updated production to calculate
        # if it will be enough for bureaucracy next turn.
        # Add a safety margin for enemy action, loss of supply chain connection could further reduce ip production.
        safety_margin = self._num_populated / 4
        if self._bureaucracy_cost + safety_margin > self._ip + self._get_infl_prod(True):
            debug(f"{self._bureaucracy_cost} + {safety_margin} <= {self._ip} + {self._get_infl_prod(True)}")

            self._deadopt(centralization)
            self._ip += self._centralization_cost

    def _try_adopt_bureaucracy(self) -> None:
        """Try to adopt bureaucracy, starting with centralization if necessary."""
        if bureaucracy in self._adoptable:
            self._adopt(bureaucracy)
        elif centralization not in self._adopted:
            self._try_adopt_centralization()
        elif self._empire.policyPrereqsAndExclusionsOK(bureaucracy):
            if self._bureaucracy_cost <= self._ip:
                # when we are here, no free slot should be the only reason, so we
                # replace centralization by bureaucracy, using a temporary slot,
                # while the game doesn't allow it directly.
                self._deadopt(infra1)
                self._adopt(bureaucracy)
                self._deadopt(centralization)
                self._adopt(infra1)

    def _maybe_deadopt_centralization(self) -> None:
        """Deadopt centralization after one turn to get rid of the IP cost and get
        the slot for technocracy or industrialism. So far, we never keep it for more than one turn."""
        turns_adopted = self._empire.turnsPoliciesAdopted
        if centralization in self._adopted and turns_adopted[centralization] != fo.currentTurn():
            # simplified: always deadopt to free the slot for technocracy
            self._deadopt(centralization)

    def _techno_or_industry(self) -> None:
        """Adopt technocracy or industrialism, depending on AI priorities."""
        research_prio = self._aistate.get_priority(PriorityType.RESOURCE_RESEARCH)
        production_prio = self._aistate.get_priority(PriorityType.RESOURCE_PRODUCTION)
        may_switch_to_techno = self._can_adopt(technocracy, industrialism)
        may_switch_to_industry = self._can_adopt(industrialism, technocracy)
        # do not switch too often
        if technocracy in self._adopted:
            research_prio *= 1.25
        elif industrialism in self._adopted:
            production_prio *= 1.25
        if may_switch_to_industry and research_prio < production_prio:
            self._deadopt(technocracy)
            self._adopt(industrialism)
        elif may_switch_to_techno and research_prio > production_prio:
            self._deadopt(industrialism)
            self._adopt(technocracy)
        debug(
            "Prio res./ind. = %.1f/%.1f, maySwitch = %s/%s",
            research_prio,
            production_prio,
            may_switch_to_techno,
            may_switch_to_industry,
        )

    def _determine_influence_priority(self, new_production: float) -> None:
        """Determine and set influence priority."""
        # avoid wildly varying priorities while we adopt the basics: simply a fixed value for some turns
        if fo.currentTurn() <= 15:
            if fo.currentTurn() == 1:
                # I'd prefer 20, but that makes Abadoni switch to Influence in turn 3.
                # TBD work on ResourceAI again...
                self._set_priority(18.0, True)
            return
        # How much IP would we have available if we keep the current production for 3 turns?
        forecast = self._ip - self._wanted_ip + 3 * new_production
        # adopting _centralization_cost costs a lot and also drops the incoming, so add 1 per populated planet
        repeated_expenses = self._centralization_cost + self._bureaucracy_cost + self._num_populated
        threshold = 20 + repeated_expenses
        if forecast < threshold:
            # Basic value: the lower the forecast, the more urgent we need influence
            priority = 20 + threshold - forecast
        else:
            # For higher values, slowly decrease priority
            priority = 20 * (threshold / forecast) ** 0.6
        # The more planets we have, the more influence we need in general, outpost have only a minor effect
        priority *= (3 + self._num_populated + self._num_outposts / 10) / 10
        self._set_priority(priority, False)

    def _wanted_for_bureaucracy(self) -> float:
        """Determine how many IP we want to reserve for the bureaucracy cycle."""
        repeated_expenses = self._centralization_cost + self._bureaucracy_cost + self._num_populated
        if fo.currentTurn() <= 10:
            # allow setup up basics (propaganda, infra1, liberty) first
            return 0.0
        if bureaucracy in self._adopted:
            # To avoid a saw tooth effect when adopting centralisation, account part of the future cost while
            # bureaucracy is adopted. Ideally IP will produce a saw tooth graph that way, while priority
            # remains relatively stable.
            turns_adopted = fo.currentTurn() - self._empire.turnsPoliciesAdopted[bureaucracy]
            return repeated_expenses * turns_adopted / self._max_turn_bureaucracy
        if centralization in self._adopted:
            # we need _bureaucracy_cost next turn, so if production is negative, we must reserve more
            return self._bureaucracy_cost - min(0, self._get_infl_prod())
        # Neither bureaucracy nor centralization adopted
        return repeated_expenses

    @staticmethod
    def _calculate_max_turn_bureaucracy() -> int:
        """Determine how many turns we can currently keep bureaucracy."""
        admin_buildings = len(BuildingType.PALACE.built_at()) + len(BuildingType.REGIONAL_ADMIN.built_at())
        turns_per_building = fo.getNamedValue("BUREAUCRACY_ADMINS_NEEDED_TURN_SCALING")
        # bureaucracy needs (turns / turns_per_building) buildings rounded down
        return (admin_buildings + 1) * turns_per_building - 1

    def _set_priority(self, calculated_priority: float, ignore_old: bool) -> None:
        """Set and log influence priority."""
        if ignore_old:
            new_priority = calculated_priority
        else:
            old_priority = self._aistate.get_priority(PriorityType.RESOURCE_INFLUENCE)
            # to further smoothen the values, only use 1/3 of the calculated value
            new_priority = (2 * old_priority + calculated_priority) / 3
        debug("Setting influence priority to %.1f, turn %d", new_priority, fo.currentTurn())
        self._aistate.set_priority(PriorityType.RESOURCE_INFLUENCE, new_priority)

    def _get_infl_prod(self, update=False) -> float:
        """Get / Update IP production."""
        if update:
            self._universe.updateMeterEstimates(self._populated_planet_ids)
            fo.updateResourcePools()
        return self._empire.resourceProduction(fo.resourceType.influence)

    def _can_adopt(self, name: str, replace: Union[str, Set[str], None] = None) -> bool:
        """
        Can we adopt named policy, possibly by replacing (one of) replace?
        Note that when replace_other is set, this function currently assumes that with
        replace_other removed, there are no other exclusions for policy(name).
        If this won't do, the function needs to temporarily deadopt replace_other or
        policyPrereqsAndExclusionsOK must be extended so that replace_other can be passed to it.
        """
        if name in self._adopted:
            return False
        policy = fo.getPolicy(name)
        wanted = 0.0 if name in self._prioritised_policies else self._wanted_ip
        ret = name in self._empire.availablePolicies and (
            policy.adoptionCost() <= (self._ip - wanted) or name in self._originally_adopted
        )
        if isinstance(replace, str) and replace in self._adopted:
            return ret
        if isinstance(replace, set) and replace & self._adopted:
            return ret
        return (
            ret and self._empire.emptyPolicySlots[policy.category] and self._empire.policyPrereqsAndExclusionsOK(name)
        )

    def _get_adoptable(self) -> Set[str]:
        """List of adoptable policies with the still available IP."""
        return {p for p in self._empire.availablePolicies if self._can_adopt(p)}

    def _adopt(self, name: str) -> None:
        """Find an emtpy slot and adopt named policy, if possible."""
        policy = fo.getPolicy(name)
        category = policy.category
        slot = self._find_empty_slot(category)
        if fo.issueAdoptPolicyOrder(name, category, slot):
            if name not in self._originally_adopted:
                self._ip -= policy.adoptionCost()
            debug(f"Issued adoption order for {name} in slot {slot} turn {fo.currentTurn()}, remaining IP: {self._ip}")
            self._adoptable = self._get_adoptable()
            self._adopted.add(name)
        else:
            error("Failed to adopt %s in slot %d", name, slot)

    def _find_empty_slot(self, category: str) -> int:
        """This assumes there is an empty slot, otherwise adopt will fail."""
        slot = 0
        # there should be a better way...
        cat_slots = self._empire.categoriesSlotPolicies
        if category in cat_slots:
            slots = cat_slots[category]
            for slot in range(0, 99):
                if slot not in slots:
                    break
        return slot

    def _deadopt(self, name: str) -> None:
        """Deadopt name, if it is adopted."""
        if name in self._adopted:
            fo.issueDeadoptPolicyOrder(name)
            self._adopted.remove(name)
            self._adoptable = self._get_adoptable()
            if name not in self._originally_adopted:
                # this is canceling an adoption order of the current turn
                self._ip += fo.getPolicy(name).adoptionCost()
            debug(f"Issued deadoption order for {name} turn {fo.currentTurn()}, remaining IP: {self._ip}")

    def _deadopt_one_of(self, names: Set[str]) -> None:
        """
        Deadopt one of the given policies and store its name.
        This can be used after a decision is made, or to temporarily deadopt one for
        decision-making. In the later case, use _readopt_selected_one() to revert it.
        """
        selection = sorted((self._rate_policy(name), name) for name in names)
        debug(f"selection = {selection}")
        for _, name in selection:
            if name in self._adopted:
                self._selected_deadopt = name
                self._deadopt(name)
                break

    def _readopt_selected_one(self) -> None:
        """Re-adopt the policy deadopted by the last call to _deadopt_one_of()."""
        self._adopt(self._selected_deadopt)

    def print_status(self) -> None:
        # only for interactive debugging
        print("\nAdoptable Policies:")
        for p in self._get_adoptable():
            print("  ", p)
        print("Empty Slots:")
        for s in self._empire.emptyPolicySlots:
            print("  ", s)
        print("Adopted:")
        for category in self._empire.categoriesSlotPolicies:
            print(" ", category.key() + ":")
            for slot in category.data():
                print("   ", slot.key(), "->", slot.data(), "turn", self._empire.turnPolicyAdopted(slot.data()))
        print(f"Influence: {self._ip} (wanted: {self._wanted_ip})")
        print("Infl. Prod.:", self._get_infl_prod())
        print("Num Planet (pop./outp.): %d/%d" % (self._num_populated, self._num_outposts))


def generate_policy_orders() -> None:
    PolicyManager().generate_orders()


def print_status() -> None:
    PolicyManager(True).print_status()
