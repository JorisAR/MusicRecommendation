class EvaluationMetrics:
    @staticmethod
    def precision(actual, recommended):
        """
        Compute precision for recommended items.

        Parameters:
        actual (list): List of actual items.
        recommended (list): List of recommended items.

        Returns:
        float: Precision value.
        """
        if len(recommended) == 0:
            print("List is empty")
            return 0
        relevant_items = set(actual) & set(recommended)
        return len(relevant_items) / len(recommended)

    @staticmethod
    def recall(actual, recommended):
        """
        Compute recall for recommended items.

        Parameters:
        actual (list): List of actual items.
        recommended (list): List of recommended items.

        Returns:
        float: Recall value.
        """
        if len(actual) == 0:
            return 0
        relevant_items = set(actual) & set(recommended)
        return len(relevant_items) / len(actual)

    @staticmethod
    def f1_score(actual, recommended):
        """
        Compute F1 score for recommended items.

        Parameters:
        actual (list): List of actual items.
        recommended (list): List of recommended items.

        Returns:
        float: F1 score value.
        """
        precision_value = EvaluationMetrics.precision(actual, recommended)
        recall_value = EvaluationMetrics.recall(actual, recommended)
        if precision_value + recall_value == 0:
            return 0
        return 2 * (precision_value * recall_value) / (precision_value + recall_value)

    @staticmethod
    def average_precision(actual, recommended):
        """
        Compute average precision for recommended items.

        Parameters:
        actual (list): List of actual items.
        recommended (list): List of recommended items.

        Returns:
        float: Average precision value.
        """
        if len(recommended) == 0 or len(actual) == 0:
            return 0
        sum_precision = 0
        num_songs = 0
        for i, item in enumerate(recommended):
            if item in actual:
                num_songs += 1
                sum_precision += num_songs / (i + 1)
        return sum_precision / len(actual)
    
    @staticmethod
    def reciprocal_rank(actual, recommended):
        """
        Compute Reciprocal Rank (RR) for recommended items.

        Parameters:
        actual (list): List of actual items.
        recommended (list): List of recommended items.

        Returns:
        float: Reciprocal Rank value.
        """
        for i, item in enumerate(recommended):
            if item in actual:
                return 1 / (i + 1)
        return 0

    @staticmethod
    def mean_reciprocal_rank(actual, recommended):
        """
        Compute Mean Reciprocal Rank (MRR) for recommended items.

        Parameters:
        actual (list): List of actual items.
        recommended (list): List of recommended items.

        Returns:
        float: Mean Reciprocal Rank value.
        """
        rr_list = [EvaluationMetrics.reciprocal_rank(a, r) for a, r in zip(actual, recommended)]
        return sum(rr_list) / len(rr_list) if rr_list else 0