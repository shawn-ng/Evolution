import gym 
from gym import spaces
import pygame 
import numpy as np

class GridWorld(gym.Env):

    """
    This is how you want your world to be rendered. 

    * try chaging the fps to see the effect.
    """
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__ (self, render_mode=None, size=10, target_number = 1):
        
        self.size = size # the size of the grid 
        self.window_size = 512

        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size-1, shape=(2,), dtype=int),
                # "target": spaces.Box(0, size-1, shape=(2,), dtype=int),
            }
        )

        for i in range(1, target_number + 1):
            self.observation_space[f"target_{i}"] = spaces.Box(0, size-1, shape=(2,), dtype=int)

        # the agent have four action 
        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([1,0]), # right
            1: np.array([0,1]), # up
            2: np.array([-1,0]), # left
            3: np.array([0,-1]) # down
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None 

    """
    This translate the environment's state into observation
    """
    def _get_obs(self):
        obs_dict = {}
        keys = [i for i in self.observation_space.keys()]
        for i in keys:
            if i == "agent":
                obs_dict[i] = self._agent_location
            else:
                obs_dict[i] = self._target_location

        if self._target_location:
            print(self._target_location)
            
        return obs_dict

    """
    We can always construct private functions to get information 
    Eg. getting the information of the distance between the agent and the food
    def _get_info(self):
        return {"distance": np.linalg.norm(self._agent_location - self._target_location, ord=1)}
    """
    
    """
    This is a mandatory function <reset>. This method will be called to initiate a new episode 
    """
    def reset(self, seed=None, option=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Choose the agent's location uniformly at random
        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        
        # Will need modification

        self._target_location = self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int
            )
    
        observation = self._get_obs()
        # info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation # , info

    """
    Step method contain the logic of the environment. It will accept
    an action and output (observation, reward, done, info).

    We can adjust the reward system 
    """
    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]

        # We use `np.clip` to make sure we don't leave the grid
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1
        )

        """
        # An episode is done iff the agent has reached the target
        Need modification:
        - the agent must return to the habitat before a certain time(night time)
        """
        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else 0  # Binary sparse rewards
        observation = self._get_obs()
        # info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False # , info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = (
            self.window_size / self.size
        )  # The size of a single grid square in pixels

        # First we draw the target
        pygame.draw.circle(
            canvas,
            (255, 0, 0),
            pix_square_size * (self._target_location + 0.5), 
            pix_square_size/ 3,
        )

        # Now we draw the agent
        pygame.draw.circle(
            canvas,
            (0, 0, 255),
            (self._agent_location + 0.5) * pix_square_size,
            pix_square_size / 3,
        )

        # Finally, add some gridlines
        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=3,
            )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
