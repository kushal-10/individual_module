"""
Evaluation Metrics
instance_score = Naive score that just evaluates if a correct action is predicted
    Could be made better to include other valid actions (If the target piece is on top-left Up and Left both should be valid

episodic_score = % Episode completed. An episode is considered 'completed' when first 'grip' action is predicted

vicinity_score = Naive score that calculates % of episodes where after all actions, does the gripper reach in the vicinity of the target piece

success_score = % episodes that are successful
A success is defined when, the location of gripper at first 'grip' action is in the vicinity of the target piece
"""

import pandas as pd

class Scorer():
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.result_df = pd.read_csv(self.file_path)
        self.result_df = self.result_df.sort_values(by=['board_numbers', 'image_numbers'], ascending=[True, True])

        self.predictions = list(self.result_df['actions'])
        self.predictions = [p.lower() for p in self.predictions]

        self.ground_truths = list(self.result_df['ground_truths'])
        self.ground_truths = [g.lower() for g in self.ground_truths]

        self.boards = list(self.result_df['board_numbers'])
        self.images = list(self.result_df['image_numbers'])

    def get_instance_score(self):
        """
        Naive scorer
        Returns:
            accuracy - % correct responses of the model, irrespective of episodes
        """

        correct_response = 0
        for prediction, ground_truth in zip(self.predictions, self.ground_truths):
            if prediction == ground_truth:
                correct_response += 1

        return correct_response / len(self.predictions)

    def get_episodic_scores(self):
        """
        Naive Episodic scorer
        Returns:
            episodic_score: % episode completed. An episode is considered as completed, when first 'grip' action is
                            generated by the model
        """

        episodes_completed = 0
        curr_episode = 0
        episodic_flag = 0
        for i in range(len(self.predictions)):
            if self.boards[i] == curr_episode:
                if self.predictions[i] == 'grip' and episodic_flag == 0:
                    episodes_completed += 1
                    episodic_flag = 1
            else:
                curr_episode += 1
                episodic_flag = 0

        return episodes_completed/(curr_episode+1)

    def increment(self, action):
        """
        Args:
            action: The action predicted by the model

        Returns:
            inc - The incremental value of the location [-1,0], [1, 0] etc ...
        """
        if action == "right":
            return [1, 0]
        elif action == "left":
            return [-1, 0]
        elif action == "up":
            return [0, 1]
        elif action == "down":
            return [0, -1]
        else:
            return [0, 0]

    def get_vicinity_score(self, vicinity: int):
        """
        Args:
            vicinity: acceptable range of the gripper's last location w.r.t the target piece
        Returns:
            vicinity_score: Defined as % of episodes in which the gripper reached a certain vicinity on its last action.
        """
        vicinity_score = 0
        curr_episode = 0
        gripper_location = [0,0]
        programmatic_location = [0,0]
        for i in range(len(self.predictions)):
            if self.boards[i] == curr_episode:
                grip_inc = self.increment(action=self.predictions[i])
                prog_inc = self.increment(action=self.ground_truths[i])
                gripper_location = [gripper_location[0] + grip_inc[0], gripper_location[1] + grip_inc[1]]
                programmatic_location = [programmatic_location[0] + prog_inc[0], programmatic_location[1] + prog_inc[1]]
            else:
                distance_x = abs(gripper_location[0] - programmatic_location[0])
                distance_y = abs(gripper_location[1] - programmatic_location[1])
                if distance_x <= vicinity and distance_y <= vicinity:
                    vicinity_score += 1
                curr_episode += 1
                gripper_location = self.increment(action=self.predictions[i])
                programmatic_location = self.increment(action=self.ground_truths[i])

        return vicinity_score/(curr_episode+1)

    def get_success_score(self, vicinity: int):
        """
        Combining previous 3 scores.
        Success is defined as the vicinity score when the episode is finished (first 'grip' action generated by the model).
        Returns:
            vicinity_score: Calculated as %episodes that are successful
        """

        success = 0
        curr_board = 0
        completion_flag = 0
        gripper_location = [0, 0]
        programmatic_location = [0, 0]
        for i in range(len(self.predictions)):
            if curr_board == self.boards[i]:
                # Update the location of gripper until grip action takes place
                if not completion_flag:
                    grip_inc = self.increment(action=self.predictions[i])
                    gripper_location = [gripper_location[0] + grip_inc[0], gripper_location[1] + grip_inc[1]]

                # Update programmatic location, to get the final location of the gripper
                prog_inc = self.increment(action=self.ground_truths[i])
                programmatic_location = [programmatic_location[0] + prog_inc[0], programmatic_location[1] + prog_inc[1]]

                if self.predictions[i] == 'grip':
                    completion_flag = 1 # Do not go again in the increment section of gripper

            else:
                distance_x = abs(gripper_location[0] - programmatic_location[0])
                distance_y = abs(gripper_location[1] - programmatic_location[1])
                if distance_x <= vicinity and distance_y <= vicinity:
                    success += 1
                gripper_location = self.increment(action=self.predictions[i])
                programmatic_location = self.increment(action=self.ground_truths[i])
                curr_board += 1
                completion_flag = 0

        return success/(curr_board+1)


if __name__ == '__main__':

    scorer = Scorer('results/adapter_prompt2.csv')
    print(scorer.get_instance_score())
    print(scorer.get_episodic_scores())
    print(scorer.get_vicinity_score(3))
    print(scorer.get_success_score(5))



