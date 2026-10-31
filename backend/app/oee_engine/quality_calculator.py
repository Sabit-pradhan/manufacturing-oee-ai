
def calculate_quality(good_count: int, total_count: int) -> float:
    """
    Quality = Good Units / Total Units

    Returns a decimal between 0 and 1.
    """

    if total_count <= 0:
        return 0.0

    if good_count < 0 or good_count > total_count:
        raise ValueError("Invalid production counts")

    return good_count / total_count
