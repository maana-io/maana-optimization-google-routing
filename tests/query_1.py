query_1 = """
{
    routingSolverMakeSchedules(
        vehicles: [{
                id: "vehicle_1"
                capacity: {
                    id: "a",
                    value: 10
                },
                volumeCapacity: {
                    id: "b",
                    value: 8
                },
                weightCapacity: {
                    id: "c",
                    value: 8
                },
                vehicleSpeed: {
                    id: "d",
                    value: 1
                },
                vehicleDimensions: {
                    id: "e",
                    depth: {
                        id: "f",
                        empty: 6,
                        massMultiplier: 1
                    }
                },
                startingLocation: {
                    id: "city_a"
                }

            },

            {
                id: "vehicle_2"
                capacity: {
                    id: "a",
                    value: 10
                },
                volumeCapacity: {
                    id: "b",
                    value: 8
                },
                weightCapacity: {
                    id: "c",
                    value: 8
                },
                vehicleSpeed: {
                    id: "d",
                    value: 1
                },
                vehicleDimensions: {
                    id: "e",
                    depth: {
                        id: "f",
                        empty: 0,
                        massMultiplier: 1
                    }
                },
                startingLocation: {
                    id: "city_a"
                }
            },
            {
                id: "vehicle_3"
                capacity: {
                    id: "a",
                    value: 20
                },
                volumeCapacity: {
                    id: "b",
                    value: 12
                },
                weightCapacity: {
                    id: "c",
                    value: 12
                },
                vehicleSpeed: {
                    id: "d",
                    value: 1
                },
                vehicleDimensions: {
                    id: "e",
                    depth: {
                        id: "f",
                        empty: 0,
                        massMultiplier: 1
                    }
                },
                startingLocation: {
                    id: "city_a"
                }
            }
        ],
        requirements: [{
                id: "cargo-1"
                routePair: {
                    id: "3",
                    origin: {
                        id: "city_a::cargo_1",
                        dimension: {
                            id: "4",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                    destination: {
                        id: "city_b::cargo_1",
                        dimension: {
                            id: "6",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                },
                volume: 2,
                weight: 2,
                revenue: 100,
                loadWindow: {
                    id: "7",
                    timeWindow: {
                        id: "8",
                        start: 1,
                        end: 3
                    }
                },
                unloadWindow: {
                    id: "9",
                    timeWindow: {
                        id: "10",
                        start: 2,
                        end: 8
                    }
                }
            },
            {
                id: "cargo-2"
                routePair: {
                    id: "3",
                    origin: {
                        id: "city_a::cargo_2",
                        dimension: {
                            id: "4",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                    destination: {
                        id: "city_d::cargo_2",
                        dimension: {
                            id: "6",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                },
                volume: 2,
                weight: 2,
                revenue: 100,
                loadWindow: {
                    id: "7",
                    timeWindow: {
                        id: "8",
                        start: 1,
                        end: 3
                    }
                },
                unloadWindow: {
                    id: "9",
                    timeWindow: {
                        id: "10",
                        start: 2,
                        end: 17
                    }
                }
            },
            {
                id: "cargo-3"
                routePair: {
                    id: "3",
                    origin: {
                        id: "city_c::cargo_3",
                        dimension: {
                            id: "4",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                    destination: {
                        id: "city_d::cargo_3",
                        dimension: {
                            id: "6",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                },
                volume: 3,
                weight: 3,
                revenue: 100,
                loadWindow: {
                    id: "7",
                    timeWindow: {
                        id: "8",
                        start: 1,
                        end: 3
                    }
                },
                unloadWindow: {
                    id: "9",
                    timeWindow: {
                        id: "10",
                        start: 11,
                        end: 20
                    }
                }
            },
            {
                id: "cargo-4"
                routePair: {
                    id: "3",
                    origin: {
                        id: "city_a::cargo_4",
                        dimension: {
                            id: "4",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                    destination: {
                        id: "city_d::cargo_4",
                        dimension: {
                            id: "6",
                            depth: {
                                id: "10",
                                max: 10
                            }
                        }
                    },
                },
                volume: 2,
                weight: 2,
                revenue: 100,
                loadWindow: {
                    id: "7",
                    timeWindow: {
                        id: "8",
                        start: 9,
                        end: 11
                    }
                },
                unloadWindow: {
                    id: "9",
                    timeWindow: {
                        id: "10",
                        start: 18,
                        end: 25
                    }
                }
            }
        ],
        costMatrix: {
            id: "11",
            costMatrices: [{
                    id: "2000"
                    rows: [{
                            id: "city_a",
                            values: [0, 6, 6, 5]
                        },
                        {
                            id: "city_b",
                            values: [6, 0, 9, 9]
                        },
                        {
                            id: "city_c",
                            values: [6, 9, 0, 7]
                        },
                        {
                            id: "city_d",
                            values: [5, 9, 7, 0]
                        }
                    ]
                },
                {
                    id: "2000"
                    rows: [{
                            id: "city_a",
                            values: [0, 5, 6, 5]
                        },
                        {
                            id: "city_b",
                            values: [5, 0, 9, 9]
                        },
                        {
                            id: "city_c",
                            values: [6, 9, 0, 8]
                        },
                        {
                            id: "city_d",
                            values: [5, 9, 8, 0]
                        }
                    ]
                },
                {
                    id: "2000"
                    rows: [{
                            id: "city_a",
                            values: [0, 5, 6, 5]
                        },
                        {
                            id: "city_b",
                            values: [5, 0, 9, 9]
                        },
                        {
                            id: "city_c",
                            values: [6, 9, 0, 8]
                        },
                        {
                            id: "city_d",
                            values: [5, 9, 8, 0]
                        }
                    ]
                }
            ],
        },
        distanceMatrix: {
            id: "17",
            rows: [{
                    id: "city_a",
                    values: [0, 5, 6, 5]
                },
                {
                    id: "city_b",
                    values: [5, 0, 9, 9]
                },
                {
                    id: "city_c",
                    values: [6, 9, 0, 8]
                },
                {
                    id: "city_d",
                    values: [5, 9, 8, 0]
                }
            ]
        },
        objective: {
            id: "22",
            firstSolutionStrategy: {
                id: "parallel_cheapest_insertion"
            },
            localSearchStrategy: {
                id: "greedy_descent"
            },
            timeLimit: 10,
            solutionLimit: 200
        }
    ) {
        id
        totalVolume
        totalCost
        totalTime
        vehicleSchedules {
            id
            timeOfRoute
            costOfRoute
            routeLoad
            profitOfRoute
            vehiclePath {
                id
                step {
                    id
                    routeNodeId
                    minTime
                    maxTime
                    cost
                    volume
                    weight
                    requirementId
                    action {
                        id
                        value
                    }
                }
            }
        }
        totalProfit
        notDeliveredRequirementIds
        notUsedVehicleIds

    }
}"""
