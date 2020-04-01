
optimizer_types = """
type Action {
  id: ID!
  value: String
}


input AddActionInput {
  id: ID
  value: String
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

input AddRequirementToTransportInput {
  id: ID
  routePair: ID
  volume: Int
  weight: Int
  loadWindow: ID
  unloadWindow: ID
  revenue: Float
  candiateVehicles: [VehicleAsInput]
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

  
  
  addCostMatrices(input: AddCostMatricesInput!): ID

  
  addCostMatricess(input: [AddCostMatricesInput]!): [ID!]!

  
  updateCostMatrices(input: UpdateCostMatricesInput!): ID

  
  updateCostMatricess(input: [UpdateCostMatricesInput]!): [ID!]!

  
  deleteCostMatrices(id: ID!): CostMatrices

  
  deleteCostMatricess(ids: [ID!]): [CostMatrices!]!

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

  
  addRouteNode(input: AddRouteNodeInput!): ID

  
  addRouteNodes(input: [AddRouteNodeInput]!): [ID!]!

  
  updateRouteNode(input: UpdateRouteNodeInput!): ID

  
  updateRouteNodes(input: [UpdateRouteNodeInput]!): [ID!]!

  
  deleteRouteNode(id: ID!): RouteNode

  
  deleteRouteNodes(ids: [ID!]): [RouteNode!]!

  
  
  addBoolVar(input: AddBoolVarInput!): ID

  
  addBoolVars(input: [AddBoolVarInput]!): [ID!]!

  
  updateBoolVar(input: UpdateBoolVarInput!): ID

  
  updateBoolVars(input: [UpdateBoolVarInput]!): [ID!]!

  
  deleteBoolVar(id: ID!): BoolVar

  
  deleteBoolVars(ids: [ID!]): [BoolVar!]!

  
  addRow(input: AddRowInput!): ID

  
  addRows(input: [AddRowInput]!): [ID!]!

  
  updateRow(input: UpdateRowInput!): ID

  
  updateRows(input: [UpdateRowInput]!): [ID!]!

  
  deleteRow(id: ID!): Row

  
  deleteRows(ids: [ID!]): [Row!]!

  
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
        objective: ObjectiveAsInput,
        routingTimeWindow: RoutingTimeWindowAsInput
        ): RoutingSolution
  
 routingSolverMakeSchedulesWithBR(
        vehicles: [VehicleAsInput],
        requirements: [RequirementToTransportAsInput], 
        costMatrix: CostMatricesAsInput,
        distanceMatrix: DistanceMatrixAsInput,
        objective: ObjectiveAsInput,
        routingTimeWindow: RoutingTimeWindowAsInput
        ): RoutingSolution
  
  routingSolverMakeSchedulesWithBRMaxProfit(
        vehicles: [VehicleAsInput],
        requirements: [RequirementToTransportAsInput], 
        costMatrix: CostMatricesAsInput,
        distanceMatrix: DistanceMatrixAsInput,
        objective: ObjectiveAsInput,
        routingTimeWindow: RoutingTimeWindowAsInput
        ): RoutingSolution
  

  
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

  
  query(input: KindQueryInput!): InstanceSet
  queryJSON(input: KindQueryInput!): String
  mipCBCSolver: String
  routingSolver(vehicles: [VehicleAsInput], requirements: [RequirementToTransportAsInput], costMatrix: CostMatricesAsInput, distanceMatrix: DistanceMatrixAsInput, objective: ObjectiveAsInput, routingTimeWindow: RoutingTimeWindowAsInput): RoutingSolution
  CKGErrors: [String]
}

type RequirementToTransport {
  id: ID!
  routePair: RoutePair
  volume: Int
  weight: Int
  loadWindow: LoadWindow
  unloadWindow: UnLoadWindow
  revenue: Float
  candiateVehicles: [Vehicle]
}

input RequirementToTransportAsInput {
  id: ID!
  routePair: RoutePairAsInput
  volume: Int
  weight: Int
  loadWindow: LoadWindowAsInput
  unloadWindow: UnLoadWindowAsInput
  revenue: Float
  candiateVehicles: [VehicleAsInput]
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
  status: String
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

type RoutingTimeWindow {
  id: ID!
  timeWindow: TimeWindow
}

input RoutingTimeWindowAsInput {
  id: ID!
  timeWindow: TimeWindowAsInput
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


input UpdateRequirementToTransportInput {
  id: ID!
  routePair: ID
  volume: Int
  weight: Int
  loadWindow: ID
  unloadWindow: ID
  revenue: Float
  candiateVehicles: [VehicleAsInput]
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
