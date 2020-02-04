
pickups_deliveries_types = """

type AssignmentConstraint {
  id: ID!
  vectorOfCoefficients: IntegerCoefficientVector
  upperBound: Int
  lowerBound: Int
  nodeSet: Boolean
}
input AssignmentConstraintAsInput {
  id: ID!
  vectorOfCoefficients: IntegerCoefficientVectorAsInput
  upperBound: Int
  lowerBound: Int
  nodeSet: Boolean
}
type AssignmentObjective {
  id: ID!
  minimize: Boolean
}
input AssignmentObjectiveAsInput {
  id: ID!
  minimize: Boolean
}
type AssignmentSolution {
  id: ID!
  nodeSetA: [Int]
  nodeSetB: [Int]
  cost: [Int]
  objectiveValue: Float
  status: String
}
type IntegerCoefficientVector {
  id: ID!
  value: [IntegerLinearCoefficient]
}
input IntegerCoefficientVectorAsInput {
  id: ID!
  value: [IntegerLinearCoefficientAsInput]
}
type CostMatrix {
  id: ID!
  row: [Row]
}
input CostMatrixAsInput {
  id: ID!
  row: [RowAsInput]
}
type Row {
  id: ID!
  values: [Int]
}
input RowAsInput {
  id: ID!
  values: [Int]
}
type CPSolution {
  id: ID!
  status: String
  objectiveValue: Int
  varValues: [IntVarValue]
}
type IntegerLinearCoefficient {
  id: ID!
  value: Int
}
input IntegerLinearCoefficientAsInput {
  id: ID!
  value: Int
}
type IntegerLinearConstraint {
  id: ID!
  upperBound: Int
  lowerBound: Int
  coefficients: [IntegerLinearCoefficient]
}
input IntegerLinearConstraintAsInput {
  id: ID!
  upperBound: Int
  lowerBound: Int
  coefficients: [IntegerLinearCoefficientAsInput]
}
type IntegerLinearObjective {
  id: ID!
  coefficients: [IntegerLinearCoefficient]
  maximize: Boolean
}
input IntegerLinearObjectiveAsInput {
  id: ID!
  coefficients: [IntegerLinearCoefficientAsInput]
  maximize: Boolean
}
type IntVar {
  id: ID!
  lowerBound: Int
  upperBound: Int
}
input IntVarAsInput {
  id: ID!
  lowerBound: Int
  upperBound: Int
}
type IntVarValue {
  id: ID!
  value: Int
}
type RealLinearCoefficient {
  id: ID!
  value: Float!
}
input RealLinearCoefficientAsInput {
  id: ID!
  value: Float!
}
type RealLinearConstraint {
  id: ID!
  lowerBound: Float
  upperBound: Float
  coefficients: [RealLinearCoefficient!]
}
input RealLinearConstraintAsInput {
  id: ID!
  lowerBound: Float
  upperBound: Float
  coefficients: [RealLinearCoefficientAsInput!]!
}
type RealLinearObjective {
  id: ID!
  coefficients: [RealLinearCoefficient!]
  maximize: Boolean!
}
input RealLinearObjectiveAsInput {
  id: ID!
  coefficients: [RealLinearCoefficientAsInput!]!
  maximize: Boolean!
}
type RealLinearSolution {
  id: ID!
  objectiveValue: Float!
  varValues: [RealLinearVarValue!]!
}
type RealLinearVar {
  id: ID!
  lowerBound: Float
  upperBound: Float
}
input RealLinearVarAsInput {
  id: ID!
  lowerBound: Float
  upperBound: Float
}
type RealLinearVarValue {
  id: ID!
  value: Float!
}


### Pickup and delivery types

type Cost {
  id: ID!
  distanceMatrix: [Row]!
}

input CostAsInput {
  id: ID!
  distanceMatrix: [RowAsInput]!
}

type PickupDelivery {
  id: ID!
  origin: Int!
  destination: Int!
}

input PickupDeliveryAsInput {
  id: ID!
  origin: Int!
  destination: Int!
}

type constraints {
  id: ID!
  numVehicles: Int!
  depot: Int!
  pickupsDeliveries: [PickupDelivery]!
}

input constraintsAsInput {
  id: ID!
  numVehicles: Int!
  depot: Int!
  pickupsDeliveries: [PickupDeliveryAsInput]!
}

type objectives {
  id: ID!
  firstSolutionStrategy: String!
  localSearchStrategy: String!
}

input objectivesAsInput {
  id: ID!
  firstSolutionStrategy: String!
  localSearchStrategy: String!
}

type VesselSchedule {
  id: ID!
  nodesToVisit: [Int!]!
}

type schedules {
  id: ID!
  vesselSchedules: [VesselSchedule!]!
}


###


type Query {
  
    solverAssignmentWithSizes(
        costs: CostMatrixAsInput, 
        constraints: [AssignmentConstraintAsInput], 
        objective: AssignmentObjectiveAsInput
        ): AssignmentSolution

    solveRealLinearProblem(
        vars: [RealLinearVarAsInput!]!,
        constraints: [RealLinearConstraintAsInput!]!,
        objective: RealLinearObjectiveAsInput!
        ): RealLinearSolution!
    
    solveLinearCPProblem(
        vars: [IntVarAsInput], 
        constraints: [IntegerLinearConstraintAsInput], 
        objective: IntegerLinearObjectiveAsInput
        ): CPSolution

    solverMakeSchedules(
        cost: CostAsInput!,
        constraints: constraintsAsInput!,
        objectives: objectivesAsInput!
        ): schedules!
                }
"""
