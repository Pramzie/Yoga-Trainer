def get_pose_feedback(user_angles, ideal_pose, threshold=15):
    feedback = []
    all_within_range = True

    for joint, ideal in ideal_pose.items():
        if joint in user_angles:
            diff = abs(user_angles[joint] - ideal)
            if diff > threshold:
                all_within_range = False
                feedback.append(f"Adjust {joint}: off by {int(diff)} degrees")
    return feedback, all_within_range
