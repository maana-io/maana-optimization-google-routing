
optimizer_types = """
type Action {
  id: ID!
  value: String
}


input AddActionInput {
  id: ID
  value: String
}


input AddAssignementConstraintXInput {
  id: ID
  bounds: ID
  coefficients: ID
}


input AddAssignmentConstraintInput {
  id: ID
  vectorOfCoefficients: ID
  upperBound: Int
  lowerBound: Int
  nodeSet: Boolean
}


input AddAssignmentObjectiveInput {
  id: ID
  minimize: Boolean
}


input AddAssignmentSolutionInput {
  id: ID
  nodeSetA: [Int]
  nodeSetB: [Int]
  cost: [Int]
  objectiveValue: Float
  status: String
}


input AddBoolVarInput {
  id: ID
  value: Boolean
}


input AddCapacityInput {
  id: ID
  value: Int
}


input AddConstraintInput {
  id: ID
  upperBound: Int
  lowerBound: Int
}


input AddConstraintUnionInput {
  id: ID
  assignemt: ID
  realLinear: ID
}


input AddCostMatricesInput {
  id: ID
  costMatrices: [ID]
}


input AddCostOfVehiclefRoutesMatrixInput {
  id: ID
  rows: [ID]
}


input AddCPSolutionInput {
  id: ID
  status: String
  objective: Int
  varValues: [ID]
}


input AddDepthInput {
  id: ID
  empty: Int
  max: Int
  massMultiplier: Int
}


input AddDimensionInput {
  id: ID
  length: Int
  width: Int
  height: Int
  depth: ID
}


input AddDistanceMatrixInput {
  id: ID
  rows: [ID]
}


input AddFirstSolutionStrategyInput {
  id: ID
}


input AddIntegerCoefficientVectorInput {
  id: ID
  value: [ID]
}


input AddIntegerLinearCoefficientInput {
  id: ID
  value: Int
}


input AddIntegerLinearConstraintInput {
  id: ID
  upperBound: Int
  lowerBound: Int
  coefficients: [ID]
}


input AddIntegerLinearObjectiveInput {
  id: ID
  coefficients: [ID]
  maximize: Boolean
}


input AddIntVarInput {
  id: ID
  lowerBound: Int
  upperBound: Int
}


input AddIntVarValueInput {
  id: ID
  value: Int
}


input AddLoadWindowInput {
  id: ID
  timeWindow: ID
}


input AddLocalSearchStrategyInput {
  id: ID
}


input AddObjectiveInput {
  id: ID
  firstSolutionStrategy: ID
  localSearchStrategy: ID
  timeLimit: Int
  solutionLimit: Int
}


input AddRealLinearCoefficientInput {
  id: ID
  value: Float!
}


input AddRealLinearConstraintInput {
  id: ID
  lowerBound: Float
  upperBound: Float
  coefficients: [ID!]
}


input AddRealLinearObjectiveInput {
  id: ID
  coefficients: [ID!]
  maximize: Boolean!
}


input AddRealLinearSolutionInput {
  id: ID
  objectiveValue: Float!
  varValues: [ID!]
}


input AddRealLinearVarInput {
  id: ID
  lowerBound: Float
  upperBound: Float
}


input AddRealLinearVarValueInput {
  id: ID
  value: Float!
}


input AddRequirementToTransportInput {
  id: ID
  routePair: ID
  volume: Int
  weight: Int
  loadWindow: ID
  unloadWindow: ID
  revenue: Float
  candiateVehicles: [ID]
}


input AddRouteNodeInput {
  id: ID
  dimension: ID
  loadTime: Int
  unLoadTime: Int
  waitTime: Int
}


input AddRoutePairInput {
  id: ID
  origin: ID
  destination: ID
}


input AddRoutingSolutionInput {
  id: ID
  totalVolume: Int
  totalCost: Int
  totalTime: Int
  totalProfit: Float
  timeWindow: ID
  notDeliveredRequirementIds: [String]
  notUsedVehicleIds: [String]
  vehicleSchedules: [ID]
}


input AddRowInput {
  id: ID
  values: [Int]
}


input AddSpeedInput {
  id: ID
  value: Int
}


input AddStepInput {
  id: ID
  routeNodeId: String
  minTime: Int
  maxTime: Int
  cost: Int
  volume: Int
  weight: Int
  requirementId: String
  action: ID
}


input AddTimeWindowInput {
  id: ID
  start: Int
  end: Int
}


input AddUnLoadWindowInput {
  id: ID
  timeWindow: ID
}


input AddVehicleInput {
  id: ID
  capacity: ID
  volumeCapacity: ID
  weightCapacity: ID
  vehicleSpeed: ID
  vehicleDimensions: ID
  startingLocation: ID
}


input AddVehiclePathInput {
  id: ID
  step: [ID]
}


input AddVehicleScheduleInput {
  id: ID
  vehiclePath: ID
  timeOfRoute: Int
  routeLoad: Int
  costOfRoute: Int
  profitOfRoute: Float
}

enum AggregateOp {
  MIN
  MAX
  SUM
  COUNT
}

type AssignementConstraintX {
  id: ID!
  bounds: Constraint
  coefficients: IntegerCoefficientVector
}

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

type BoolVar {
  id: ID!
  value: Boolean
}

type Capacity {
  id: ID!
  value: Int
}

input CapacityAsInput {
  id: ID!
  value: Int
}

type Constraint {
  id: ID!
  upperBound: Int
  lowerBound: Int
}

type ConstraintUnion {
  id: ID!
  assignemt: AssignementConstraintX
  realLinear: RealLinearConstraint
}

type CostMatrices {
  id: ID!
  costMatrices: [CostOfVehiclefRoutesMatrix]
}

input CostMatricesAsInput {
  id: ID!
  costMatrices: [CostOfVehiclefRoutesMatrixAsInput]
}

type CostOfVehiclefRoutesMatrix {
  id: ID!
  rows: [Row]
}

input CostOfVehiclefRoutesMatrixAsInput {
  id: ID!
  rows: [RowAsInput]
}

type CPSolution {
  id: ID!
  status: String
  objective: Int
  varValues: [IntVarValue]
}

scalar Date

scalar DateTime

type Depth {
  id: ID!
  empty: Int
  max: Int
  massMultiplier: Int
}

input DepthAsInput {
  id: ID!
  empty: Int
  max: Int
  massMultiplier: Int
}

type Dimension {
  id: ID!
  length: Int
  width: Int
  height: Int
  depth: Depth
}

input DimensionAsInput {
  id: ID!
  length: Int
  width: Int
  height: Int
  depth: DepthAsInput
}

type DistanceMatrix {
  id: ID!
  rows: [Row]
}

input DistanceMatrixAsInput {
  id: ID!
  rows: [RowAsInput]
}

input FieldFilterInput {
  
  fieldId: ID
  fieldName: String
  op: String!
  value: FieldValueInput!
}

input FieldProjectionInput {
  
  fieldId: ID
  fieldName: String

  
  alias: String
  op: AggregateOp
}

type FieldValue {
  
  ID: ID
  STRING: String
  INT: Int
  FLOAT: Float
  BOOLEAN: Boolean
  DATE: Date
  TIME: Time
  DATETIME: DateTime
  JSON: JSON
  KIND: ID

  
  l_ID: [ID]
  l_STRING: [String]
  l_INT: [Int]
  l_FLOAT: [Float]
  l_BOOLEAN: [Boolean]
  l_DATE: [Date]
  l_TIME: [Time]
  l_DATETIME: [DateTime]
  l_JSON: [JSON]
  l_KIND: [ID]
}

input FieldValueInput {
  
  ID: ID
  STRING: String
  INT: Int
  FLOAT: Float
  BOOLEAN: Boolean
  DATE: Date
  TIME: Time
  DATETIME: DateTime
  JSON: JSON
  KIND: ID

  
  l_ID: [ID]
  l_STRING: [String]
  l_INT: [Int]
  l_FLOAT: [Float]
  l_BOOLEAN: [Boolean]
  l_DATE: [Date]
  l_TIME: [Time]
  l_DATETIME: [DateTime]
  l_JSON: [JSON]
  l_KIND: [ID]
}

type FirstSolutionStrategy {
  id: ID!
}

input FirstSolutionStrategyAsInput {
  id: ID!
}

type Info {
  id: ID!
  name: String!
  description: String
}

type InstanceSet {
  kindId: ID!

  
  token: String
  fieldIds: [ID]

  
  records: [[FieldValue]]
}

type IntegerCoefficientVector {
  id: ID!
  value: [IntegerLinearCoefficient]
}

input IntegerCoefficientVectorAsInput {
  id: ID!
  value: [IntegerLinearCoefficientAsInput]
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

scalar JSON

input KindQueryInput {
  
  kindId: ID
  kindName: String
  serviceId: ID

  
  alias: String

  
  projection: [FieldProjectionInput]

  
  distinct: Boolean

  
  fieldFilters: [FieldFilterInput]

  
  and: [KindQueryInput]

  
  or: [KindQueryInput]

  
  fromFieldId: ID
  fromFieldName: String
  toFieldId: ID
  toFieldName: String
  take: Int
  token: String
}

type LoadWindow {
  id: ID!
  timeWindow: TimeWindow
}

input LoadWindowAsInput {
  id: ID!
  timeWindow: TimeWindowAsInput
}

type LocalSearchStrategy {
  id: ID!
}

input LocalSearchStrategyAsInput {
  id: ID!
}

type Mutation {
  
  addRealLinearConstraint(input: AddRealLinearConstraintInput!): ID

  
  addRealLinearConstraints(input: [AddRealLinearConstraintInput]!): [ID!]!

  
  updateRealLinearConstraint(input: UpdateRealLinearConstraintInput!): ID

  
  updateRealLinearConstraints(input: [UpdateRealLinearConstraintInput]!): [ID!]!

  
  deleteRealLinearConstraint(id: ID!): RealLinearConstraint

  
  deleteRealLinearConstraints(ids: [ID!]): [RealLinearConstraint!]!

  
  addAssignementConstraintX(input: AddAssignementConstraintXInput!): ID

  
  addAssignementConstraintXs(input: [AddAssignementConstraintXInput]!): [ID!]!

  
  updateAssignementConstraintX(input: UpdateAssignementConstraintXInput!): ID

  
  updateAssignementConstraintXs(input: [UpdateAssignementConstraintXInput]!): [ID!]!

  
  deleteAssignementConstraintX(id: ID!): AssignementConstraintX

  
  deleteAssignementConstraintXs(ids: [ID!]): [AssignementConstraintX!]!

  
  addRoutingSolution(input: AddRoutingSolutionInput!): ID

  
  addRoutingSolutions(input: [AddRoutingSolutionInput]!): [ID!]!

  
  updateRoutingSolution(input: UpdateRoutingSolutionInput!): ID

  
  updateRoutingSolutions(input: [UpdateRoutingSolutionInput]!): [ID!]!

  
  deleteRoutingSolution(id: ID!): RoutingSolution

  
  deleteRoutingSolutions(ids: [ID!]): [RoutingSolution!]!

  
  addFirstSolutionStrategy(input: AddFirstSolutionStrategyInput!): ID

  
  addFirstSolutionStrategys(input: [AddFirstSolutionStrategyInput]!): [ID!]!

  
  updateFirstSolutionStrategy(input: UpdateFirstSolutionStrategyInput!): ID

  
  updateFirstSolutionStrategys(input: [UpdateFirstSolutionStrategyInput]!): [ID!]!

  
  deleteFirstSolutionStrategy(id: ID!): FirstSolutionStrategy

  
  deleteFirstSolutionStrategys(ids: [ID!]): [FirstSolutionStrategy!]!

  
  addIntVar(input: AddIntVarInput!): ID

  
  addIntVars(input: [AddIntVarInput]!): [ID!]!

  
  updateIntVar(input: UpdateIntVarInput!): ID

  
  updateIntVars(input: [UpdateIntVarInput]!): [ID!]!

  
  deleteIntVar(id: ID!): IntVar

  
  deleteIntVars(ids: [ID!]): [IntVar!]!

  
  addIntegerLinearCoefficient(input: AddIntegerLinearCoefficientInput!): ID

  
  addIntegerLinearCoefficients(input: [AddIntegerLinearCoefficientInput]!): [ID!]!

  
  updateIntegerLinearCoefficient(input: UpdateIntegerLinearCoefficientInput!): ID

  
  updateIntegerLinearCoefficients(input: [UpdateIntegerLinearCoefficientInput]!): [ID!]!

  
  deleteIntegerLinearCoefficient(id: ID!): IntegerLinearCoefficient

  
  deleteIntegerLinearCoefficients(ids: [ID!]): [IntegerLinearCoefficient!]!

  
  addCostMatrices(input: AddCostMatricesInput!): ID

  
  addCostMatricess(input: [AddCostMatricesInput]!): [ID!]!

  
  updateCostMatrices(input: UpdateCostMatricesInput!): ID

  
  updateCostMatricess(input: [UpdateCostMatricesInput]!): [ID!]!

  
  deleteCostMatrices(id: ID!): CostMatrices

  
  deleteCostMatricess(ids: [ID!]): [CostMatrices!]!

  
  addAssignmentObjective(input: AddAssignmentObjectiveInput!): ID

  
  addAssignmentObjectives(input: [AddAssignmentObjectiveInput]!): [ID!]!

  
  updateAssignmentObjective(input: UpdateAssignmentObjectiveInput!): ID

  
  updateAssignmentObjectives(input: [UpdateAssignmentObjectiveInput]!): [ID!]!

  
  deleteAssignmentObjective(id: ID!): AssignmentObjective

  
  deleteAssignmentObjectives(ids: [ID!]): [AssignmentObjective!]!

  
  addRoutePair(input: AddRoutePairInput!): ID

  
  addRoutePairs(input: [AddRoutePairInput]!): [ID!]!

  
  updateRoutePair(input: UpdateRoutePairInput!): ID

  
  updateRoutePairs(input: [UpdateRoutePairInput]!): [ID!]!

  
  deleteRoutePair(id: ID!): RoutePair

  
  deleteRoutePairs(ids: [ID!]): [RoutePair!]!

  
  addTimeWindow(input: AddTimeWindowInput!): ID

  
  addTimeWindows(input: [AddTimeWindowInput]!): [ID!]!

  
  updateTimeWindow(input: UpdateTimeWindowInput!): ID

  
  updateTimeWindows(input: [UpdateTimeWindowInput]!): [ID!]!

  
  deleteTimeWindow(id: ID!): TimeWindow

  
  deleteTimeWindows(ids: [ID!]): [TimeWindow!]!

  
  addCostOfVehiclefRoutesMatrix(input: AddCostOfVehiclefRoutesMatrixInput!): ID

  
  addCostOfVehiclefRoutesMatrixs(input: [AddCostOfVehiclefRoutesMatrixInput]!): [ID!]!

  
  updateCostOfVehiclefRoutesMatrix(input: UpdateCostOfVehiclefRoutesMatrixInput!): ID

  
  updateCostOfVehiclefRoutesMatrixs(input: [UpdateCostOfVehiclefRoutesMatrixInput]!): [ID!]!

  
  deleteCostOfVehiclefRoutesMatrix(id: ID!): CostOfVehiclefRoutesMatrix

  
  deleteCostOfVehiclefRoutesMatrixs(ids: [ID!]): [CostOfVehiclefRoutesMatrix!]!

  
  addRequirementToTransport(input: AddRequirementToTransportInput!): ID

  
  addRequirementToTransports(input: [AddRequirementToTransportInput]!): [ID!]!

  
  updateRequirementToTransport(input: UpdateRequirementToTransportInput!): ID

  
  updateRequirementToTransports(input: [UpdateRequirementToTransportInput]!): [ID!]!

  
  deleteRequirementToTransport(id: ID!): RequirementToTransport

  
  deleteRequirementToTransports(ids: [ID!]): [RequirementToTransport!]!

  
  addUnLoadWindow(input: AddUnLoadWindowInput!): ID

  
  addUnLoadWindows(input: [AddUnLoadWindowInput]!): [ID!]!

  
  updateUnLoadWindow(input: UpdateUnLoadWindowInput!): ID

  
  updateUnLoadWindows(input: [UpdateUnLoadWindowInput]!): [ID!]!

  
  deleteUnLoadWindow(id: ID!): UnLoadWindow

  
  deleteUnLoadWindows(ids: [ID!]): [UnLoadWindow!]!

  
  addVehicle(input: AddVehicleInput!): ID

  
  addVehicles(input: [AddVehicleInput]!): [ID!]!

  
  updateVehicle(input: UpdateVehicleInput!): ID

  
  updateVehicles(input: [UpdateVehicleInput]!): [ID!]!

  
  deleteVehicle(id: ID!): Vehicle

  
  deleteVehicles(ids: [ID!]): [Vehicle!]!

  
  addDistanceMatrix(input: AddDistanceMatrixInput!): ID

  
  addDistanceMatrixs(input: [AddDistanceMatrixInput]!): [ID!]!

  
  updateDistanceMatrix(input: UpdateDistanceMatrixInput!): ID

  
  updateDistanceMatrixs(input: [UpdateDistanceMatrixInput]!): [ID!]!

  
  deleteDistanceMatrix(id: ID!): DistanceMatrix

  
  deleteDistanceMatrixs(ids: [ID!]): [DistanceMatrix!]!

  
  addSpeed(input: AddSpeedInput!): ID

  
  addSpeeds(input: [AddSpeedInput]!): [ID!]!

  
  updateSpeed(input: UpdateSpeedInput!): ID

  
  updateSpeeds(input: [UpdateSpeedInput]!): [ID!]!

  
  deleteSpeed(id: ID!): Speed

  
  deleteSpeeds(ids: [ID!]): [Speed!]!

  
  addVehicleSchedule(input: AddVehicleScheduleInput!): ID

  
  addVehicleSchedules(input: [AddVehicleScheduleInput]!): [ID!]!

  
  updateVehicleSchedule(input: UpdateVehicleScheduleInput!): ID

  
  updateVehicleSchedules(input: [UpdateVehicleScheduleInput]!): [ID!]!

  
  deleteVehicleSchedule(id: ID!): VehicleSchedule

  
  deleteVehicleSchedules(ids: [ID!]): [VehicleSchedule!]!

  
  addLoadWindow(input: AddLoadWindowInput!): ID

  
  addLoadWindows(input: [AddLoadWindowInput]!): [ID!]!

  
  updateLoadWindow(input: UpdateLoadWindowInput!): ID

  
  updateLoadWindows(input: [UpdateLoadWindowInput]!): [ID!]!

  
  deleteLoadWindow(id: ID!): LoadWindow

  
  deleteLoadWindows(ids: [ID!]): [LoadWindow!]!

  
  addAction(input: AddActionInput!): ID

  
  addActions(input: [AddActionInput]!): [ID!]!

  
  updateAction(input: UpdateActionInput!): ID

  
  updateActions(input: [UpdateActionInput]!): [ID!]!

  
  deleteAction(id: ID!): Action

  
  deleteActions(ids: [ID!]): [Action!]!

  
  addDepth(input: AddDepthInput!): ID

  
  addDepths(input: [AddDepthInput]!): [ID!]!

  
  updateDepth(input: UpdateDepthInput!): ID

  
  updateDepths(input: [UpdateDepthInput]!): [ID!]!

  
  deleteDepth(id: ID!): Depth

  
  deleteDepths(ids: [ID!]): [Depth!]!

  
  addLocalSearchStrategy(input: AddLocalSearchStrategyInput!): ID

  
  addLocalSearchStrategys(input: [AddLocalSearchStrategyInput]!): [ID!]!

  
  updateLocalSearchStrategy(input: UpdateLocalSearchStrategyInput!): ID

  
  updateLocalSearchStrategys(input: [UpdateLocalSearchStrategyInput]!): [ID!]!

  
  deleteLocalSearchStrategy(id: ID!): LocalSearchStrategy

  
  deleteLocalSearchStrategys(ids: [ID!]): [LocalSearchStrategy!]!

  
  addIntVarValue(input: AddIntVarValueInput!): ID

  
  addIntVarValues(input: [AddIntVarValueInput]!): [ID!]!

  
  updateIntVarValue(input: UpdateIntVarValueInput!): ID

  
  updateIntVarValues(input: [UpdateIntVarValueInput]!): [ID!]!

  
  deleteIntVarValue(id: ID!): IntVarValue

  
  deleteIntVarValues(ids: [ID!]): [IntVarValue!]!

  
  addAssignmentSolution(input: AddAssignmentSolutionInput!): ID

  
  addAssignmentSolutions(input: [AddAssignmentSolutionInput]!): [ID!]!

  
  updateAssignmentSolution(input: UpdateAssignmentSolutionInput!): ID

  
  updateAssignmentSolutions(input: [UpdateAssignmentSolutionInput]!): [ID!]!

  
  deleteAssignmentSolution(id: ID!): AssignmentSolution

  
  deleteAssignmentSolutions(ids: [ID!]): [AssignmentSolution!]!

  
  addDimension(input: AddDimensionInput!): ID

  
  addDimensions(input: [AddDimensionInput]!): [ID!]!

  
  updateDimension(input: UpdateDimensionInput!): ID

  
  updateDimensions(input: [UpdateDimensionInput]!): [ID!]!

  
  deleteDimension(id: ID!): Dimension

  
  deleteDimensions(ids: [ID!]): [Dimension!]!

  
  addVehiclePath(input: AddVehiclePathInput!): ID

  
  addVehiclePaths(input: [AddVehiclePathInput]!): [ID!]!

  
  updateVehiclePath(input: UpdateVehiclePathInput!): ID

  
  updateVehiclePaths(input: [UpdateVehiclePathInput]!): [ID!]!

  
  deleteVehiclePath(id: ID!): VehiclePath

  
  deleteVehiclePaths(ids: [ID!]): [VehiclePath!]!

  
  addRealLinearObjective(input: AddRealLinearObjectiveInput!): ID

  
  addRealLinearObjectives(input: [AddRealLinearObjectiveInput]!): [ID!]!

  
  updateRealLinearObjective(input: UpdateRealLinearObjectiveInput!): ID

  
  updateRealLinearObjectives(input: [UpdateRealLinearObjectiveInput]!): [ID!]!

  
  deleteRealLinearObjective(id: ID!): RealLinearObjective

  
  deleteRealLinearObjectives(ids: [ID!]): [RealLinearObjective!]!

  
  addIntegerCoefficientVector(input: AddIntegerCoefficientVectorInput!): ID

  
  addIntegerCoefficientVectors(input: [AddIntegerCoefficientVectorInput]!): [ID!]!

  
  updateIntegerCoefficientVector(input: UpdateIntegerCoefficientVectorInput!): ID

  
  updateIntegerCoefficientVectors(input: [UpdateIntegerCoefficientVectorInput]!): [ID!]!

  
  deleteIntegerCoefficientVector(id: ID!): IntegerCoefficientVector

  
  deleteIntegerCoefficientVectors(ids: [ID!]): [IntegerCoefficientVector!]!

  
  addObjective(input: AddObjectiveInput!): ID

  
  addObjectives(input: [AddObjectiveInput]!): [ID!]!

  
  updateObjective(input: UpdateObjectiveInput!): ID

  
  updateObjectives(input: [UpdateObjectiveInput]!): [ID!]!

  
  deleteObjective(id: ID!): Objective

  
  deleteObjectives(ids: [ID!]): [Objective!]!

  
  addStep(input: AddStepInput!): ID

  
  addSteps(input: [AddStepInput]!): [ID!]!

  
  updateStep(input: UpdateStepInput!): ID

  
  updateSteps(input: [UpdateStepInput]!): [ID!]!

  
  deleteStep(id: ID!): Step

  
  deleteSteps(ids: [ID!]): [Step!]!

  
  addCPSolution(input: AddCPSolutionInput!): ID

  
  addCPSolutions(input: [AddCPSolutionInput]!): [ID!]!

  
  updateCPSolution(input: UpdateCPSolutionInput!): ID

  
  updateCPSolutions(input: [UpdateCPSolutionInput]!): [ID!]!

  
  deleteCPSolution(id: ID!): CPSolution

  
  deleteCPSolutions(ids: [ID!]): [CPSolution!]!

  
  addConstraintUnion(input: AddConstraintUnionInput!): ID

  
  addConstraintUnions(input: [AddConstraintUnionInput]!): [ID!]!

  
  updateConstraintUnion(input: UpdateConstraintUnionInput!): ID

  
  updateConstraintUnions(input: [UpdateConstraintUnionInput]!): [ID!]!

  
  deleteConstraintUnion(id: ID!): ConstraintUnion

  
  deleteConstraintUnions(ids: [ID!]): [ConstraintUnion!]!

  
  addRealLinearVarValue(input: AddRealLinearVarValueInput!): ID

  
  addRealLinearVarValues(input: [AddRealLinearVarValueInput]!): [ID!]!

  
  updateRealLinearVarValue(input: UpdateRealLinearVarValueInput!): ID

  
  updateRealLinearVarValues(input: [UpdateRealLinearVarValueInput]!): [ID!]!

  
  deleteRealLinearVarValue(id: ID!): RealLinearVarValue

  
  deleteRealLinearVarValues(ids: [ID!]): [RealLinearVarValue!]!

  
  addRouteNode(input: AddRouteNodeInput!): ID

  
  addRouteNodes(input: [AddRouteNodeInput]!): [ID!]!

  
  updateRouteNode(input: UpdateRouteNodeInput!): ID

  
  updateRouteNodes(input: [UpdateRouteNodeInput]!): [ID!]!

  
  deleteRouteNode(id: ID!): RouteNode

  
  deleteRouteNodes(ids: [ID!]): [RouteNode!]!

  
  addRealLinearVar(input: AddRealLinearVarInput!): ID

  
  addRealLinearVars(input: [AddRealLinearVarInput]!): [ID!]!

  
  updateRealLinearVar(input: UpdateRealLinearVarInput!): ID

  
  updateRealLinearVars(input: [UpdateRealLinearVarInput]!): [ID!]!

  
  deleteRealLinearVar(id: ID!): RealLinearVar

  
  deleteRealLinearVars(ids: [ID!]): [RealLinearVar!]!

  
  addRealLinearCoefficient(input: AddRealLinearCoefficientInput!): ID

  
  addRealLinearCoefficients(input: [AddRealLinearCoefficientInput]!): [ID!]!

  
  updateRealLinearCoefficient(input: UpdateRealLinearCoefficientInput!): ID

  
  updateRealLinearCoefficients(input: [UpdateRealLinearCoefficientInput]!): [ID!]!

  
  deleteRealLinearCoefficient(id: ID!): RealLinearCoefficient

  
  deleteRealLinearCoefficients(ids: [ID!]): [RealLinearCoefficient!]!

  
  addBoolVar(input: AddBoolVarInput!): ID

  
  addBoolVars(input: [AddBoolVarInput]!): [ID!]!

  
  updateBoolVar(input: UpdateBoolVarInput!): ID

  
  updateBoolVars(input: [UpdateBoolVarInput]!): [ID!]!

  
  deleteBoolVar(id: ID!): BoolVar

  
  deleteBoolVars(ids: [ID!]): [BoolVar!]!

  
  addRealLinearSolution(input: AddRealLinearSolutionInput!): ID

  
  addRealLinearSolutions(input: [AddRealLinearSolutionInput]!): [ID!]!

  
  updateRealLinearSolution(input: UpdateRealLinearSolutionInput!): ID

  
  updateRealLinearSolutions(input: [UpdateRealLinearSolutionInput]!): [ID!]!

  
  deleteRealLinearSolution(id: ID!): RealLinearSolution

  
  deleteRealLinearSolutions(ids: [ID!]): [RealLinearSolution!]!

  
  addRow(input: AddRowInput!): ID

  
  addRows(input: [AddRowInput]!): [ID!]!

  
  updateRow(input: UpdateRowInput!): ID

  
  updateRows(input: [UpdateRowInput]!): [ID!]!

  
  deleteRow(id: ID!): Row

  
  deleteRows(ids: [ID!]): [Row!]!

  
  addAssignmentConstraint(input: AddAssignmentConstraintInput!): ID

  
  addAssignmentConstraints(input: [AddAssignmentConstraintInput]!): [ID!]!

  
  updateAssignmentConstraint(input: UpdateAssignmentConstraintInput!): ID

  
  updateAssignmentConstraints(input: [UpdateAssignmentConstraintInput]!): [ID!]!

  
  deleteAssignmentConstraint(id: ID!): AssignmentConstraint

  
  deleteAssignmentConstraints(ids: [ID!]): [AssignmentConstraint!]!

  
  addIntegerLinearConstraint(input: AddIntegerLinearConstraintInput!): ID

  
  addIntegerLinearConstraints(input: [AddIntegerLinearConstraintInput]!): [ID!]!

  
  updateIntegerLinearConstraint(input: UpdateIntegerLinearConstraintInput!): ID

  
  updateIntegerLinearConstraints(input: [UpdateIntegerLinearConstraintInput]!): [ID!]!

  
  deleteIntegerLinearConstraint(id: ID!): IntegerLinearConstraint

  
  deleteIntegerLinearConstraints(ids: [ID!]): [IntegerLinearConstraint!]!

  
  addIntegerLinearObjective(input: AddIntegerLinearObjectiveInput!): ID

  
  addIntegerLinearObjectives(input: [AddIntegerLinearObjectiveInput]!): [ID!]!

  
  updateIntegerLinearObjective(input: UpdateIntegerLinearObjectiveInput!): ID

  
  updateIntegerLinearObjectives(input: [UpdateIntegerLinearObjectiveInput]!): [ID!]!

  
  deleteIntegerLinearObjective(id: ID!): IntegerLinearObjective

  
  deleteIntegerLinearObjectives(ids: [ID!]): [IntegerLinearObjective!]!

  
  addConstraint(input: AddConstraintInput!): ID

  
  addConstraints(input: [AddConstraintInput]!): [ID!]!

  
  updateConstraint(input: UpdateConstraintInput!): ID

  
  updateConstraints(input: [UpdateConstraintInput]!): [ID!]!

  
  deleteConstraint(id: ID!): Constraint

  
  deleteConstraints(ids: [ID!]): [Constraint!]!

  
  addCapacity(input: AddCapacityInput!): ID

  
  addCapacitys(input: [AddCapacityInput]!): [ID!]!

  
  updateCapacity(input: UpdateCapacityInput!): ID

  
  updateCapacitys(input: [UpdateCapacityInput]!): [ID!]!

  
  deleteCapacity(id: ID!): Capacity

  
  deleteCapacitys(ids: [ID!]): [Capacity!]!

  
  clearCache: Boolean!
}

type Objective {
  id: ID!
  firstSolutionStrategy: FirstSolutionStrategy
  localSearchStrategy: LocalSearchStrategy
  timeLimit: Int
  solutionLimit: Int
}

input ObjectiveAsInput {
  id: ID!
  firstSolutionStrategy: FirstSolutionStrategyAsInput
  localSearchStrategy: LocalSearchStrategyAsInput
  timeLimit: Int
  solutionLimit: Int
}

type Query {

    # routingSolverMakeSchedules(
    #     vehicles: [VehicleAsInput]
    # ): Int

  routingSolverMakeSchedules(
        vehicles: [VehicleAsInput],
        requirements: [RequirementToTransportAsInput], 
        costMatrix: CostMatricesAsInput,
        distanceMatrix: DistanceMatrixAsInput,
        objective: ObjectiveAsInput
        ): RoutingSolution
  
  allRealLinearConstraints(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearConstraint!]!

  
  realLinearConstraint(id: ID!): RealLinearConstraint

  
  realLinearConstraints(ids: [ID]!): [RealLinearConstraint!]!

  
  realLinearConstraintFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearConstraint!]!

  
  allAssignementConstraintXs(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignementConstraintX!]!

  
  assignementConstraintX(id: ID!): AssignementConstraintX

  
  assignementConstraintXs(ids: [ID]!): [AssignementConstraintX!]!

  
  assignementConstraintXFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignementConstraintX!]!

  
  allRoutingSolutions(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RoutingSolution!]!

  
  routingSolution(id: ID!): RoutingSolution

  
  routingSolutions(ids: [ID]!): [RoutingSolution!]!

  
  routingSolutionFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RoutingSolution!]!

  
  allFirstSolutionStrategys(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [FirstSolutionStrategy!]!

  
  firstSolutionStrategy(id: ID!): FirstSolutionStrategy

  
  firstSolutionStrategys(ids: [ID]!): [FirstSolutionStrategy!]!

  
  firstSolutionStrategyFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [FirstSolutionStrategy!]!

  
  allIntVars(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntVar!]!

  
  intVar(id: ID!): IntVar

  
  intVars(ids: [ID]!): [IntVar!]!

  
  intVarFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntVar!]!

  
  allIntegerLinearCoefficients(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerLinearCoefficient!]!

  
  integerLinearCoefficient(id: ID!): IntegerLinearCoefficient

  
  integerLinearCoefficients(ids: [ID]!): [IntegerLinearCoefficient!]!

  
  integerLinearCoefficientFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerLinearCoefficient!]!

  
  allCostMatricess(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [CostMatrices!]!

  
  costMatrices(id: ID!): CostMatrices

  
  costMatricess(ids: [ID]!): [CostMatrices!]!

  
  costMatricesFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [CostMatrices!]!

  
  allAssignmentObjectives(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignmentObjective!]!

  
  assignmentObjective(id: ID!): AssignmentObjective

  
  assignmentObjectives(ids: [ID]!): [AssignmentObjective!]!

  
  assignmentObjectiveFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignmentObjective!]!

  
  allRoutePairs(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RoutePair!]!

  
  routePair(id: ID!): RoutePair

  
  routePairs(ids: [ID]!): [RoutePair!]!

  
  routePairFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RoutePair!]!

  
  allTimeWindows(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [TimeWindow!]!

  
  timeWindow(id: ID!): TimeWindow

  
  timeWindows(ids: [ID]!): [TimeWindow!]!

  
  timeWindowFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [TimeWindow!]!

  
  allCostOfVehiclefRoutesMatrixs(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [CostOfVehiclefRoutesMatrix!]!

  
  costOfVehiclefRoutesMatrix(id: ID!): CostOfVehiclefRoutesMatrix

  
  costOfVehiclefRoutesMatrixs(ids: [ID]!): [CostOfVehiclefRoutesMatrix!]!

  
  costOfVehiclefRoutesMatrixFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [CostOfVehiclefRoutesMatrix!]!

  
  allRequirementToTransports(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RequirementToTransport!]!

  
  requirementToTransport(id: ID!): RequirementToTransport

  
  requirementToTransports(ids: [ID]!): [RequirementToTransport!]!

  
  requirementToTransportFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RequirementToTransport!]!

  
  allUnLoadWindows(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [UnLoadWindow!]!

  
  unLoadWindow(id: ID!): UnLoadWindow

  
  unLoadWindows(ids: [ID]!): [UnLoadWindow!]!

  
  unLoadWindowFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [UnLoadWindow!]!

  
  allVehicles(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Vehicle!]!

  
  vehicle(id: ID!): Vehicle

  
  vehicles(ids: [ID]!): [Vehicle!]!

  
  vehicleFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Vehicle!]!

  
  allDistanceMatrixs(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [DistanceMatrix!]!

  
  distanceMatrix(id: ID!): DistanceMatrix

  
  distanceMatrixs(ids: [ID]!): [DistanceMatrix!]!

  
  distanceMatrixFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [DistanceMatrix!]!

  
  allSpeeds(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Speed!]!

  
  speed(id: ID!): Speed

  
  speeds(ids: [ID]!): [Speed!]!

  
  speedFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Speed!]!

  
  allVehicleSchedules(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [VehicleSchedule!]!

  
  vehicleSchedule(id: ID!): VehicleSchedule

  
  vehicleSchedules(ids: [ID]!): [VehicleSchedule!]!

  
  vehicleScheduleFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [VehicleSchedule!]!

  
  allLoadWindows(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [LoadWindow!]!

  
  loadWindow(id: ID!): LoadWindow

  
  loadWindows(ids: [ID]!): [LoadWindow!]!

  
  loadWindowFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [LoadWindow!]!

  
  allActions(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Action!]!

  
  action(id: ID!): Action

  
  actions(ids: [ID]!): [Action!]!

  
  actionFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Action!]!

  
  allDepths(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Depth!]!

  
  depth(id: ID!): Depth

  
  depths(ids: [ID]!): [Depth!]!

  
  depthFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Depth!]!

  
  allLocalSearchStrategys(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [LocalSearchStrategy!]!

  
  localSearchStrategy(id: ID!): LocalSearchStrategy

  
  localSearchStrategys(ids: [ID]!): [LocalSearchStrategy!]!

  
  localSearchStrategyFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [LocalSearchStrategy!]!

  
  allIntVarValues(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntVarValue!]!

  
  intVarValue(id: ID!): IntVarValue

  
  intVarValues(ids: [ID]!): [IntVarValue!]!

  
  intVarValueFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntVarValue!]!

  
  allAssignmentSolutions(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignmentSolution!]!

  
  assignmentSolution(id: ID!): AssignmentSolution

  
  assignmentSolutions(ids: [ID]!): [AssignmentSolution!]!

  
  assignmentSolutionFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignmentSolution!]!

  
  allDimensions(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Dimension!]!

  
  dimension(id: ID!): Dimension

  
  dimensions(ids: [ID]!): [Dimension!]!

  
  dimensionFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Dimension!]!

  
  allVehiclePaths(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [VehiclePath!]!

  
  vehiclePath(id: ID!): VehiclePath

  
  vehiclePaths(ids: [ID]!): [VehiclePath!]!

  
  vehiclePathFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [VehiclePath!]!

  
  allRealLinearObjectives(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearObjective!]!

  
  realLinearObjective(id: ID!): RealLinearObjective

  
  realLinearObjectives(ids: [ID]!): [RealLinearObjective!]!

  
  realLinearObjectiveFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearObjective!]!

  
  allIntegerCoefficientVectors(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerCoefficientVector!]!

  
  integerCoefficientVector(id: ID!): IntegerCoefficientVector

  
  integerCoefficientVectors(ids: [ID]!): [IntegerCoefficientVector!]!

  
  integerCoefficientVectorFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerCoefficientVector!]!

  
  allObjectives(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Objective!]!

  
  objective(id: ID!): Objective

  
  objectives(ids: [ID]!): [Objective!]!

  
  objectiveFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Objective!]!

  
  allSteps(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Step!]!

  
  step(id: ID!): Step

  
  steps(ids: [ID]!): [Step!]!

  
  stepFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Step!]!

  
  allCPSolutions(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [CPSolution!]!

  
  cPSolution(id: ID!): CPSolution

  
  cPSolutions(ids: [ID]!): [CPSolution!]!

  
  cPSolutionFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [CPSolution!]!

  
  allConstraintUnions(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [ConstraintUnion!]!

  
  constraintUnion(id: ID!): ConstraintUnion

  
  constraintUnions(ids: [ID]!): [ConstraintUnion!]!

  
  constraintUnionFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [ConstraintUnion!]!

  
  allRealLinearVarValues(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearVarValue!]!

  
  realLinearVarValue(id: ID!): RealLinearVarValue

  
  realLinearVarValues(ids: [ID]!): [RealLinearVarValue!]!

  
  realLinearVarValueFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearVarValue!]!

  
  allRouteNodes(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RouteNode!]!

  
  routeNode(id: ID!): RouteNode

  
  routeNodes(ids: [ID]!): [RouteNode!]!

  
  routeNodeFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RouteNode!]!

  
  allRealLinearVars(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearVar!]!

  
  realLinearVar(id: ID!): RealLinearVar

  
  realLinearVars(ids: [ID]!): [RealLinearVar!]!

  
  realLinearVarFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearVar!]!

  
  allRealLinearCoefficients(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearCoefficient!]!

  
  realLinearCoefficient(id: ID!): RealLinearCoefficient

  
  realLinearCoefficients(ids: [ID]!): [RealLinearCoefficient!]!

  
  realLinearCoefficientFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearCoefficient!]!

  
  allBoolVars(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [BoolVar!]!

  
  boolVar(id: ID!): BoolVar

  
  boolVars(ids: [ID]!): [BoolVar!]!

  
  boolVarFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [BoolVar!]!

  
  allRealLinearSolutions(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearSolution!]!

  
  realLinearSolution(id: ID!): RealLinearSolution

  
  realLinearSolutions(ids: [ID]!): [RealLinearSolution!]!

  
  realLinearSolutionFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [RealLinearSolution!]!

  
  allRows(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Row!]!

  
  row(id: ID!): Row

  
  rows(ids: [ID]!): [Row!]!

  
  rowFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Row!]!

  
  allAssignmentConstraints(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignmentConstraint!]!

  
  assignmentConstraint(id: ID!): AssignmentConstraint

  
  assignmentConstraints(ids: [ID]!): [AssignmentConstraint!]!

  
  assignmentConstraintFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [AssignmentConstraint!]!

  
  allIntegerLinearConstraints(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerLinearConstraint!]!

  
  integerLinearConstraint(id: ID!): IntegerLinearConstraint

  
  integerLinearConstraints(ids: [ID]!): [IntegerLinearConstraint!]!

  
  integerLinearConstraintFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerLinearConstraint!]!

  
  allIntegerLinearObjectives(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerLinearObjective!]!

  
  integerLinearObjective(id: ID!): IntegerLinearObjective

  
  integerLinearObjectives(ids: [ID]!): [IntegerLinearObjective!]!

  
  integerLinearObjectiveFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [IntegerLinearObjective!]!

  
  allConstraints(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Constraint!]!

  
  constraint(id: ID!): Constraint

  
  constraints(ids: [ID]!): [Constraint!]!

  
  constraintFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Constraint!]!

  
  allCapacitys(
    
    take: Int = 1000

    
    offset: Int = 0
  ): [Capacity!]!

  
  capacity(id: ID!): Capacity

  
  capacitys(ids: [ID]!): [Capacity!]!

  
  capacityFilter(
    filters: [FieldFilterInput]!

    
    take: Int = 1000

    
    offset: Int = 0
  ): [Capacity!]!

  
  info: Info!

  
  query(input: KindQueryInput!): InstanceSet
  queryJSON(input: KindQueryInput!): String
  solveLinearCPProblem(vars: [IntVarAsInput], constraints: [IntegerLinearConstraintAsInput], objective: IntegerLinearObjectiveAsInput): CPSolution
  mipCBCSolver: String
  routingSolver(vehicles: [VehicleAsInput], requirements: [RequirementToTransportAsInput], costMatrix: CostMatricesAsInput, distanceMatrix: DistanceMatrixAsInput, objective: ObjectiveAsInput): RoutingSolution
  solveRealLinearProblem(vars: [RealLinearVarAsInput!]!, constraints: [RealLinearConstraintAsInput!]!, objective: RealLinearObjectiveAsInput!): RealLinearSolution!
  solverAssignmentWithSizes(costs: CostMatricesAsInput, constraints: [AssignmentConstraintAsInput], objective: AssignmentObjectiveAsInput): AssignmentSolution
  CKGErrors: [String]
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

type RequirementToTransport {
  id: ID!
  routePair: RoutePair
  volume: Int
  weight: Int
  loadWindow: LoadWindow
  unloadWindow: UnLoadWindow
  revenue: Float
  candiateVehicles: [String]
}

input RequirementToTransportAsInput {
  id: ID!
  routePair: RoutePairAsInput
  volume: Int
  weight: Int
  loadWindow: LoadWindowAsInput
  unloadWindow: UnLoadWindowAsInput
  revenue: Float
  candiateVehicles: [String]
}

type RouteNode {
  id: ID!
  dimension: Dimension
  loadTime: Int
  unLoadTime: Int
  waitTime: Int
}

input RouteNodeAsInput {
  id: ID!
  dimension: DimensionAsInput
  loadTime: Int
  unLoadTime: Int
  waitTime: Int
}

type RoutePair {
  id: ID!
  origin: RouteNode
  destination: RouteNode
}

input RoutePairAsInput {
  id: ID!
  origin: RouteNodeAsInput
  destination: RouteNodeAsInput
}

type RoutingSolution {
  id: ID!
  totalVolume: Int
  totalCost: Int
  totalTime: Int
  totalProfit: Float
  timeWindow: TimeWindow
  notDeliveredRequirementIds: [String]
  notUsedVehicleIds: [String]
  vehicleSchedules: [VehicleSchedule]
}

type Row {
  id: ID!
  values: [Int]
}

input RowAsInput {
  id: ID!
  values: [Int]
}

type Speed {
  id: ID!
  value: Int
}

input SpeedAsInput {
  id: ID!
  value: Int
}

type Step {
  id: ID!
  routeNodeId: String
  minTime: Int
  maxTime: Int
  cost: Int
  volume: Int
  weight: Int
  requirementId: String
  action: Action
}

scalar Time

type TimeWindow {
  id: ID!
  start: Int
  end: Int
}

input TimeWindowAsInput {
  id: ID!
  start: Int
  end: Int
}

type UnLoadWindow {
  id: ID!
  timeWindow: TimeWindow
}

input UnLoadWindowAsInput {
  id: ID!
  timeWindow: TimeWindowAsInput
}


input UpdateActionInput {
  id: ID!
  value: String
}


input UpdateAssignementConstraintXInput {
  id: ID!
  bounds: ID
  coefficients: ID
}


input UpdateAssignmentConstraintInput {
  id: ID!
  vectorOfCoefficients: ID
  upperBound: Int
  lowerBound: Int
  nodeSet: Boolean
}


input UpdateAssignmentObjectiveInput {
  id: ID!
  minimize: Boolean
}


input UpdateAssignmentSolutionInput {
  id: ID!
  nodeSetA: [Int]
  nodeSetB: [Int]
  cost: [Int]
  objectiveValue: Float
  status: String
}


input UpdateBoolVarInput {
  id: ID!
  value: Boolean
}


input UpdateCapacityInput {
  id: ID!
  value: Int
}


input UpdateConstraintInput {
  id: ID!
  upperBound: Int
  lowerBound: Int
}


input UpdateConstraintUnionInput {
  id: ID!
  assignemt: ID
  realLinear: ID
}


input UpdateCostMatricesInput {
  id: ID!
  costMatrices: [ID]
}


input UpdateCostOfVehiclefRoutesMatrixInput {
  id: ID!
  rows: [ID]
}


input UpdateCPSolutionInput {
  id: ID!
  status: String
  objective: Int
  varValues: [ID]
}


input UpdateDepthInput {
  id: ID!
  empty: Int
  max: Int
  massMultiplier: Int
}


input UpdateDimensionInput {
  id: ID!
  length: Int
  width: Int
  height: Int
  depth: ID
}


input UpdateDistanceMatrixInput {
  id: ID!
  rows: [ID]
}


input UpdateFirstSolutionStrategyInput {
  id: ID!
}


input UpdateIntegerCoefficientVectorInput {
  id: ID!
  value: [ID]
}


input UpdateIntegerLinearCoefficientInput {
  id: ID!
  value: Int
}


input UpdateIntegerLinearConstraintInput {
  id: ID!
  upperBound: Int
  lowerBound: Int
  coefficients: [ID]
}


input UpdateIntegerLinearObjectiveInput {
  id: ID!
  coefficients: [ID]
  maximize: Boolean
}


input UpdateIntVarInput {
  id: ID!
  lowerBound: Int
  upperBound: Int
}


input UpdateIntVarValueInput {
  id: ID!
  value: Int
}


input UpdateLoadWindowInput {
  id: ID!
  timeWindow: ID
}


input UpdateLocalSearchStrategyInput {
  id: ID!
}


input UpdateObjectiveInput {
  id: ID!
  firstSolutionStrategy: ID
  localSearchStrategy: ID
  timeLimit: Int
  solutionLimit: Int
}


input UpdateRealLinearCoefficientInput {
  id: ID!
  value: Float
}


input UpdateRealLinearConstraintInput {
  id: ID!
  lowerBound: Float
  upperBound: Float
  coefficients: [ID]
}


input UpdateRealLinearObjectiveInput {
  id: ID!
  coefficients: [ID]
  maximize: Boolean
}


input UpdateRealLinearSolutionInput {
  id: ID!
  objectiveValue: Float
  varValues: [ID]
}


input UpdateRealLinearVarInput {
  id: ID!
  lowerBound: Float
  upperBound: Float
}


input UpdateRealLinearVarValueInput {
  id: ID!
  value: Float
}


input UpdateRequirementToTransportInput {
  id: ID!
  routePair: ID
  volume: Int
  weight: Int
  loadWindow: ID
  unloadWindow: ID
  revenue: Float
  candiateVehicles: [ID]
}


input UpdateRouteNodeInput {
  id: ID!
  dimension: ID
  loadTime: Int
  unLoadTime: Int
  waitTime: Int
}


input UpdateRoutePairInput {
  id: ID!
  origin: ID
  destination: ID
}


input UpdateRoutingSolutionInput {
  id: ID!
  totalVolume: Int
  totalCost: Int
  totalTime: Int
  totalProfit: Float
  timeWindow: ID
  notDeliveredRequirementIds: [String]
  notUsedVehicleIds: [String]
  vehicleSchedules: [ID]
}


input UpdateRowInput {
  id: ID!
  values: [Int]
}


input UpdateSpeedInput {
  id: ID!
  value: Int
}


input UpdateStepInput {
  id: ID!
  routeNodeId: String
  minTime: Int
  maxTime: Int
  cost: Int
  volume: Int
  weight: Int
  requirementId: String
  action: ID
}


input UpdateTimeWindowInput {
  id: ID!
  start: Int
  end: Int
}


input UpdateUnLoadWindowInput {
  id: ID!
  timeWindow: ID
}


input UpdateVehicleInput {
  id: ID!
  capacity: ID
  volumeCapacity: ID
  weightCapacity: ID
  vehicleSpeed: ID
  vehicleDimensions: ID
  startingLocation: ID
}


input UpdateVehiclePathInput {
  id: ID!
  step: [ID]
}


input UpdateVehicleScheduleInput {
  id: ID!
  vehiclePath: ID
  timeOfRoute: Int
  routeLoad: Int
  costOfRoute: Int
  profitOfRoute: Float
}

type Vehicle {
  id: ID!
  capacity: Capacity
  volumeCapacity: Capacity
  weightCapacity: Capacity
  vehicleSpeed: Speed
  vehicleDimensions: Dimension
  startingLocation: RouteNode
}

input VehicleAsInput {
  id: ID!
  capacity: CapacityAsInput
  volumeCapacity: CapacityAsInput
  weightCapacity: CapacityAsInput
  vehicleSpeed: SpeedAsInput
  vehicleDimensions: DimensionAsInput
  startingLocation: RouteNodeAsInput
}

type VehiclePath {
  id: ID!
  step: [Step]
}

type VehicleSchedule {
  id: ID!
  vehiclePath: VehiclePath
  timeOfRoute: Int
  routeLoad: Int
  costOfRoute: Int
  profitOfRoute: Float
}

"""
