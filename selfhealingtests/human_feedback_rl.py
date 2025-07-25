from collections import deque
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback

class HumanFeedbackRL:
    def __init__(self, model):
        self.model = model
        self.memory = deque(maxlen=5000)
        self.optimizer = PPO(
            policy="MlpPolicy",
            model=self.model,
            verbose=1
        )
    
    def record_decision(self, element, action, human_decision):
        reward = 1.0 if action == human_decision else -0.2
        self.memory.append((element, action, reward))
        if len(self.memory) > 100:
            self._update_model()
    
    def _update_model(self):
        states, actions, rewards = zip(*self.memory)
        self.optimizer.learn(
            total_timesteps=1000,
            callback=[EvalCallback(self.model)]
        ) 