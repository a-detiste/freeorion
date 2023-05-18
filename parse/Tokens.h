#ifndef _Tokens_h_
#define _Tokens_h_

#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/seq/for_each.hpp>

#define TOKEN_SEQ_1                             \
    (abs)                                       \
    (accountinglabel)                           \
    (activation)                                \
    (AddSpecial)                                \
    (AddStarlanes)                              \
    (Adequate)                                  \
    (adoptioncost)                              \
    (affiliation)                               \
    (Age)                                       \
    (Aggressive)                                \
    (All)                                       \
    (AllyOf)                                    \
    (And)                                       \
    (annexationcondition)                       \
    (annexationcost)                            \
    (AnyEmpire)                                 \
    (Armed)                                     \
    (Armour)                                    \
    (ArrivedOnTurn)                             \
    (Article)                                   \
    (Asteroids)                                 \
    (Barren)                                    \
    (Basic)                                     \
    (BlackHole)                                 \
    (Blue)                                      \
    (Bombard)                                   \
    (buildcost)

#define TOKEN_SEQ_2                             \
    (Building)                                  \
    (BuildingTypesOwned)                        \
    (BuildingType)                              \
    (BuildingTypesProduced)                     \
    (BuildingTypesScrapped)                     \
    (buildtime)                                 \
    (CanAddStarlanesTo)                         \
    (CanColonize)                               \
    (CanProduceShips)                           \
    (CanSee)                                    \
    (capacity)                                  \
    (Capacity)                                  \
    (Capital)                                   \
    (Capture)                                   \
    (carrier)                                   \
    (captureresult)                             \
    (category)                                  \
    (ceil)                                      \
    (class)                                     \
    (ClockwiseNextPlanetType)                   \
    (Colony)                                    \
    (colour)                                    \
    (CombatBout)                                \
    (combatTargets)                             \
    (condition)                                 \
    (Construction)                              \
    (consumption)                               \
    (ContainedBy)                               \
    (ContainerID)                               \
    (Contains)                                  \
    (Core)                                      \
    (cos)                                       \
    (Count)                                     \
    (CountUnique)                               \
    (CounterClockwiseNextPlanetType)            \
    (CreateBuilding)                            \
    (CreatedOnTurn)                             \
    (CreateField)                               \
    (CreatePlanet)                              \
    (CreateShip)                                \
    (CreateSystem)                              \
    (CreationTurn)                              \
    (CumulativeTurnsPolicyAdopted)              \
    (CurrentContent)                            \
    (CurrentTurn)

#define TOKEN_SEQ_3                             \
    (damage)                                    \
    (Damage)                                    \
    (damageStructurePerBattleMax)               \
    (DamageStructurePerBattleMax)               \
    (data)                                      \
    (default)                                   \
    (defaultfocus)                              \
    (DefaultFocus)                              \
    (Defense)                                   \
    (Described)                                 \
    (description)                               \
    (Desert)                                    \
    (design)                                    \
    (Design)                                    \
    (DesignHasHull)                             \
    (DesignHasPart)                             \
    (DesignHasPartClass)                        \
    (designid)                                  \
    (DesignID)                                  \
    (designname)                                \
    (destination)                               \
    (Destroy)                                   \
    (destroyFightersPerBattleMax)               \
    (DestroyFightersPerBattleMax)               \
    (Detection)                                 \
    (DirectDistanceBetween)                     \
    (dislikes)                                  \
    (distance)                                  \
    (DistanceFromOriginalType)                  \
    (effects)                                   \
    (EffectsGroup)                              \
    (effectsgroups)                             \
    (else)                                      \
    (empire)                                    \
    (EmpireHasAdoptedPolicy)                    \
    (EmpireHasBuildingAvailable)                \
    (EmpireHasShipDesignAvailable)              \
    (EmpireHasShipPartAvailable)                \
    (EmpireMeter)                               \
    (EmpireMeterValue)                          \
    (EmpireObjectVisibility)                    \
    (EmpireShipsDestroyed)                      \
    (EmpireStockpile)                           \
    (endpoint)                                  \
    (EnemyOf)                                   \
    (Enqueued)                                  \
    (enqueuelocation)                           \
    (environment)                               \
    (Environment)                               \
    (environments)                              \
    (ETA)                                       \
    (ExploredByEmpire)                          \
    (exclusions)                                \
    (External)

#define TOKEN_SEQ_4                             \
    (Field)                                     \
    (FieldType)                                 \
    (Fighter)                                   \
    (FighterBay)                                \
    (FighterHangar)                             \
    (FighterWeapon)                             \
    (FinalDestinationID)                        \
    (Fleet)                                     \
    (FleetID)                                   \
    (floor)                                     \
    (foci)                                      \
    (focus)                                     \
    (Focus)                                     \
    (from)                                      \
    (fuel)                                      \
    (Fuel)                                      \
    (Full)                                      \
    (GalaxyAge)                                 \
    (GalaxyMaxAIAggression)                     \
    (GalaxyMonsterFrequency)                    \
    (GalaxyNativeFrequency)                     \
    (GalaxyPlanetDensity)                       \
    (GalaxySeed)                                \
    (GalaxyShape)                               \
    (GalaxySize)                                \
    (GalaxySpecialFrequency)                    \
    (GalaxyStarlaneFrequency)                   \
    (gameplay_description)                      \
    (GameRule)                                  \
    (GasGiant)                                  \
    (General)

#define TOKEN_SEQ_5                             \
    (GenerateSitRepMessage)                     \
    (GiveEmpireTech)                            \
    (Good)                                      \
    (graphic)                                   \
    (HabitableSize)                             \
    (Happiness)                                 \
    (HasSpecial)                                \
    (HasSpecialCapacity)                        \
    (HasSpecialSinceTurn)                       \
    (HasTag)                                    \
    (high)                                      \
    (HighestCostEnqueuedTech)                   \
    (HighestCostResearchableTech)               \
    (HighestCostTransferrableTech)              \
    (HistogramMax)                              \
    (HistogramMin)                              \
    (HistogramSpread)                           \
    (Homeworld)                                 \
    (Hostile)                                   \
    (Huge)                                      \
    (hull)                                      \
    (Hull)                                      \
    (HullFuel)                                  \
    (HullSpeed)                                 \
    (HullStealth)                               \
    (HullStructure)                             \
    (Human)                                     \
    (icon)                                      \
    (id)                                        \
    (ID)                                        \
    (If)                                        \
    (Industry)                                  \
    (Inferno)                                   \
    (Influence)                                 \
    (InSystem)                                  \
    (Integer)                                   \
    (Internal)                                  \
    (Invisible)                                 \
    (Item)                                      \
    (jumps)                                     \
    (JumpsBetween)

#define TOKEN_SEQ_6                             \
    (label)                                     \
    (Large)                                     \
    (LastTurnActiveInBattle)                    \
    (LastTurnAnnexed)                           \
    (LastTurnAttackedByShip)                    \
    (LastTurnBattleHere)                        \
    (LastTurnColonized)                         \
    (LastTurnConquered)                         \
    (LastTurnMoveOrdered)                       \
    (LastTurnResupplied)                        \
    (LaunchedFrom)                              \
    (LeastHappySpecies)                         \
    (likes)                                     \
    (LocalCandidate)                            \
    (location)                                  \
    (Location)                                  \
    (log)                                       \
    (Lookup)                                    \
    (low)                                       \
    (LowestCostEnqueuedTech)                    \
    (LowestCostResearchableTech)                \
    (LowestCostTransferrableTech)               \
    (max)                                       \
    (Max)                                       \
    (MaxCapacity)                               \
    (MaxDamage)                                 \
    (MaxDefense)                                \
    (MaxFuel)                                   \
    (MaximumNumberOf)                           \
    (MaxSecondaryStat)                          \
    (MaxShield)                                 \
    (MaxStockpile)                              \
    (MaxStructure)                              \
    (MaxSupply)                                 \
    (MaxTroops)                                 \
    (Mean)                                      \
    (Medium)                                    \
    (message)                                   \
    (meter)                                     \
    (min)                                       \
    (Min)                                       \
    (MinimumNumberOf)

#define TOKEN_SEQ_7                             \
    (Mode)                                      \
    (model)                                     \
    (ModeNumberOf)                              \
    (Monster)                                   \
    (MonsterFleet)                              \
    (MostHappySpecies)                          \
    (MostPopulousSpecies)                       \
    (MostSpentEnqueuedTech)                     \
    (MostSpentResearchableTech)                 \
    (MostSpentTransferrableTech)                \
    (mountableSlotTypes)                        \
    (MoveInOrbit)                               \
    (MoveTo)                                    \
    (MoveTowards)                               \
    (name)                                      \
    (Name)                                      \
    (Named)                                     \
    (Native)                                    \
    (NearestSystemID)                           \
    (Neutron)                                   \
    (NextBestPlanetType)                        \
    (NextBetterPlanetType)                      \
    (NextCloserToOriginalPlanetType)            \
    (NextLargerPlanetSize)                      \
    (NextSmallerPlanetSize)                     \
    (NextOlderStarType)                         \
    (NextSystemID)                              \
    (NextYoungerStarType)                       \
    (NoDefaultCapacityEffect)                   \
    (NoDefaultFuelEffect)                       \
    (NoDefaultSpeedEffect)                      \
    (NoDefaultStealthEffect)                    \
    (NoDefaultStructureEffect)                  \
    (None)                                      \
    (NoOp)                                      \
    (NoStar)                                    \
    (NoStringtableLookup)                       \
    (Not)                                       \
    (number)                                    \
    (Number)                                    \
    (NumberOf)                                  \
    (NumPoliciesAdopted)                        \
    (NumShips)                                  \
    (NumStarlanes)

#define TOKEN_SEQ_8                             \
    (object)                                    \
    (Object)                                    \
    (ObjectType)                                \
    (Ocean)                                     \
    (On)                                        \
    (OneOf)                                     \
    (OnPlanet)                                  \
    (opinion)                                   \
    (Or)                                        \
    (Orange)                                    \
    (Orbit)                                     \
    (OrderedAlternativesOf)                     \
    (OrderedBombardedBy)                        \
    (OrderedColonizePlanetID)                   \
    (OriginalType)                              \
    (OutpostsOwned)                             \
    (OwnedBy)                                   \
    (Owner)                                     \
    (OwnerHasShipPartAvailable)                 \
    (OwnerHasTech)                              \
    (parameters)                                \
    (part)                                      \
    (Part)                                      \
    (PartCapacity)                              \
    (PartClass)                                 \
    (Partial)                                   \
    (partname)                                  \
    (PartSecondaryStat)

#define TOKEN_SEQ_9                             \
    (parts)                                     \
    (PartOfClassInShipDesign)                   \
    (PartsInShipDesign)                         \
    (Passive)                                   \
    (PeaceWith)                                 \
    (Planet)                                    \
    (PlanetEnvironment)                         \
    (PlanetID)                                  \
    (planetsize)                                \
    (PlanetType)                                \
    (PlanetTypeDifference)                      \
    (Playable)                                  \
    (Policy)                                    \
    (Poor)                                      \
    (Population)                                \
    (PopulationCenter)                          \
    (position)                                  \
    (prerequisites)                             \
    (PreviousSystemID)                          \
    (PreviousToFinalDestinationID)              \
    (priority)                                  \
    (probability)                               \
    (ProducedByEmpire)                          \
    (ProducedByEmpireID)                        \
    (Producible)                                \
    (Product)                                   \
    (ProductionCenter)                          \
    (ProductionLocation)                        \
    (PropagatedSupplyRange)                     \
    (Property)                                  \
    (progress)

#define TOKEN_SEQ_10                            \
    (Radiated)                                  \
    (Random)                                    \
    (RandomColonizableSpecies)                  \
    (RandomCompleteTech)                        \
    (RandomControlledSpecies)                   \
    (RandomEnqueuedTech)                        \
    (RandomResearchableTech)                    \
    (RandomTransferrableTech)                   \
    (RandomNumber)                              \
    (Range)                                     \
    (Real)                                      \
    (reason)                                    \
    (RebelTroops)                               \
    (Red)                                       \
    (RemoveSpecial)                             \
    (RemoveStarlanes)                           \
    (Research)                                  \
    (researchcost)                              \
    (researchturns)                             \
    (resource)                                  \
    (ResourceSupplyConnected)                   \
    (ResupplyableBy)                            \
    (Retain)                                    \
    (RMS)                                       \
    (RootCandidate)                             \
    (round)                                     \
    (scope)                                     \
    (SecondaryStat)

#define TOKEN_SEQ_11                            \
    (SetAggressive)                             \
    (SetCapacity)                               \
    (SetConstruction)                           \
    (SetDamage)                                 \
    (SetDefense)                                \
    (SetDefensive)                              \
    (SetDestination)                            \
    (SetDetection)                              \
    (SetEmpireCapital)                          \
    (SetEmpireMeter)                            \
    (SetEmpireTechProgress)                     \
    (SetEmpireStockpile)                        \
    (SetFuel)                                   \
    (SetHappiness)                              \
    (SetIndustry)                               \
    (SetInfluence)                              \
    (SetMaxCapacity)                            \
    (SetMaxDamage)                              \
    (SetMaxDefense)                             \
    (SetMaxFuel)                                \
    (SetMaxSecondaryStat)                       \
    (SetMaxShield)                              \
    (SetMaxStockpile)                           \
    (SetMaxStructure)                           \
    (SetMaxSupply)                              \
    (SetMaxTroops)                              \
    (SetObstructive)                            \
    (SetOriginalType)                           \
    (SetOverlayTexture)                         \
    (SetOwner)                                  \
    (SetPassive)                                \
    (SetPlanetSize)                             \
    (SetPlanetType)                             \
    (SetPopulation)

#define TOKEN_SEQ_12                            \
    (SetRebelTroops)                            \
    (SetResearch)                               \
    (SetSecondaryStat)                          \
    (SetShield)                                 \
    (SetSize)                                   \
    (SetSpecialCapacity)                        \
    (SetSpecies)                                \
    (SetSpeciesOpinion)                         \
    (SetSpeciesTargetOpinion)                   \
    (SetSpeed)                                  \
    (SetStarType)                               \
    (SetStealth)                                \
    (SetStockpile)                              \
    (SetStructure)                              \
    (SetSupply)                                 \
    (SetTargetConstruction)                     \
    (SetTargetHappiness)                        \
    (SetTargetIndustry)                         \
    (SetTargetInfluence)                        \
    (SetTargetPopulation)                       \
    (SetTargetResearch)                         \
    (SetTexture)                                \
    (SetTroops)                                 \
    (SetVisibility)

#define TOKEN_SEQ_13                            \
    (Shield)                                    \
    (ShipDesign)                                \
    (ShipDesignCost)                            \
    (ShipDesignOrdering)                        \
    (ShipDesignsDestroyed)                      \
    (ShipDesignsInProduction)                   \
    (ShipDesignsLost)                           \
    (ShipDesignsOwned)                          \
    (ShipDesignsProduced)                       \
    (ShipDesignsScrapped)                       \
    (Ship)                                      \
    (ShipHull)                                  \
    (ShipPart)                                  \
    (ShipPartMeter)                             \
    (ShipPartsOwned)                            \
    (ships)                                     \
    (short_description)                         \
    (ShortestPath)                              \
    (ShortRange)                                \
    (shots)                                     \
    (sign)                                      \
    (sin)                                       \
    (size)                                      \
    (Size)                                      \
    (SizeAsDouble)

#define TOKEN_SEQ_14                            \
    (Slot)                                      \
    (slots)                                     \
    (SlotsInHull)                               \
    (SlotsInShipDesign)                         \
    (Small)                                     \
    (sortkey)                                   \
    (Source)                                    \
    (spawnlimit)                                \
    (spawnrate)                                 \
    (Special)                                   \
    (SpecialAddedOnTurn)                        \
    (SpecialCapacity)                           \
    (species)                                   \
    (Species)                                   \
    (SpeciesCensusOrdering)                     \
    (SpeciesColoniesOwned)                      \
    (SpeciesContentOpinion)                     \
    (SpeciesDislikes)                           \
    (SpeciesEmpireOpinion)                      \
    (SpeciesEmpireTargetOpinion)                \
    (SpeciesLikes)                              \
    (SpeciesSpeciesOpinion)                     \
    (SpeciesSpeciesTargetOpinion)               \
    (SpeciesPlanetsBombed)

#define TOKEN_SEQ_15                            \
    (SpeciesPlanetsDepoped)                     \
    (SpeciesPlanetsInvaded)                     \
    (SpeciesShipsDestroyed)                     \
    (SpeciesShipsLost)                          \
    (SpeciesShipsOwned)                         \
    (SpeciesShipsProduced)                      \
    (SpeciesShipsScrapped)                      \
    (speed)                                     \
    (Speed)                                     \
    (Spread)                                    \
    (stackinggroup)                             \
    (Star)                                      \
    (StarType)                                  \
    (Stationary)                                \
    (Statistic)                                 \
    (StDev)                                     \
    (stealth)                                   \
    (Stealth)                                   \
    (Stockpile)                                 \
    (String)                                    \
    (structure)                                 \
    (Structure)                                 \
    (Sum)                                       \
    (Supply)                                    \
    (SupplyingEmpire)                           \
    (Swamp)                                     \
    (System)                                    \
    (SystemID)

#define TOKEN_SEQ_16                            \
    (tag)                                       \
    (tags)                                      \
    (target)                                    \
    (Target)                                    \
    (TargetConstruction)                        \
    (TargetHappiness)                           \
    (TargetIndustry)                            \
    (TargetInfluence)                           \
    (TargetPopulation)                          \
    (TargetResearch)                            \
    (Tech)                                      \
    (Terran)                                    \
    (TheEmpire)                                 \
    (ThisBuilding)                              \
    (ThisField)                                 \
    (ThisHull)                                  \
    (ThisPart)                                  \
    (ThisPolicy)                                \
    (ThisTech)                                  \
    (ThisSpecies)                               \
    (ThisSpecial)                               \
    (Tiny)                                      \
    (TopPriorityEnqueuedTech)                   \
    (TopPriorityResearchableTech)               \
    (TopPriorityTransferrableTech)              \
    (TotalFighterShots)                         \
    (to)                                        \
    (Toxic)

#define TOKEN_SEQ_17                            \
    (Troops)                                    \
    (Tundra)                                    \
    (turn)                                      \
    (Turn)                                      \
    (TurnPolicyAdopted)                         \
    (TurnsSinceAnnexation)                      \
    (TurnsSinceColonization)                    \
    (TurnsSinceFocusChange)                     \
    (TurnsSinceLastConquered)                   \
    (TurnsSincePolicyAdopted)                   \
    (TurnSystemExplored)                        \
    (TurnTechResearched)                        \
    (type)                                      \
    (Uninhabitable)                             \
    (UniqueNumberOf)                            \
    (Unique)                                    \
    (UniverseCentreX)                           \
    (UniverseCentreY)                           \
    (UniverseWidth)                             \
    (UnlockBuildingType)                        \
    (UnlockPolicy)                              \
    (UnlockShipHull)                            \
    (UnlockShipPart)                            \
    (unlock)                                    \
    (Unowned)                                   \
    (Unproducible)                              \
    (UsedInDesignID)                            \
    (UserString)                                \
    (uuid)                                      \
    (value)                                     \
    (Value)                                     \
    (Victory)                                   \
    (VisibleToEmpire)                           \
    (visibility)                                \
    (White)                                     \
    (WithinDistance)                            \
    (WithinStarlaneJumps)                       \
    (x)                                         \
    (X)                                         \
    (y)                                         \
    (Y)                                         \
    (Yellow)

#endif
