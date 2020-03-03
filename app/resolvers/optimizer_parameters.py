
class Parameters:
    def __init__(
        self,
        time_slack=500,
        time_capacity=10000,
        time_fix_cumul_to_zero=False,
        cost_slack=0,
        cost_capacity=1000 * 1000 * 1000,
        cost_fix_cumul_to_zero=False,
        draft_slack=0,
        draft_capacity=1000 * 1000,
        draft_fix_cumul_to_zero=True,
        volume_slack=0,
        volume_fix_cumul_to_zero=True,
        weight_slack=0,
        weight_fix_cumul_to_zero=True,
        punishment_for_missing_cargo=1000*1000*1000


    ):
        self.time_slack = time_slack
        self.time_capacity = time_capacity
        self.time_fix_cumul_to_zero = time_fix_cumul_to_zero
        self.cost_slack = cost_slack
        self.cost_capacity = cost_capacity
        self.cost_fix_cumul_to_zero = cost_fix_cumul_to_zero
        self.draft_slack = draft_slack
        self.draft_capacity = draft_capacity
        self.draft_fix_cumul_to_zero = draft_fix_cumul_to_zero
        self.volume_slack = volume_slack
        self.volume_fix_cumul_to_zero = volume_fix_cumul_to_zero
        self.weight_slack = weight_slack
        self.weight_fix_cumul_to_zero = weight_fix_cumul_to_zero
        self.punishment_for_missing_cargo = punishment_for_missing_cargo


parameters = Parameters()
