# Stone Dodge AI

Stone Dodge AI is a game built with Pygame where players control a character dodging rocks falling from the sky. This project implements a neural network to train AI agents, enabling them to learn the best strategies for survival using NEAT (NeuroEvolution of Augmenting Topologies). The AI leverages NEAT-Python to evolve networks over generations, optimizing the agent's ability to dodge falling obstacles.

## Table of Contents
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [Game Controls](#game-controls)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Getting Started

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Makankn/stoneDodgeAI.git
    cd stoneDodgeAI
    ```

2. **Install dependencies**:
    Ensure you have Python installed, then install the required packages:
    ```bash
    pip install pygame numpy neat-python
    ```

3. **Run the game**:
    ```bash
    python stone_dodge_ai.py
    ```

## How It Works

This project uses NEAT (NeuroEvolution of Augmenting Topologies) to train AI agents to dodge obstacles effectively. Each agent (player character) receives inputs representing game state information, including:
- The player’s position relative to the screen edges.
- The position and speed of the closest and second-closest rocks.
- Whether the player is moving left, right, or staying still.

The NEAT algorithm then evolves networks over generations, with each network representing an agent’s brain. The agents are rewarded based on their survival time and penalized for collisions or lack of movement, encouraging optimal dodge behavior over generations.

## Game Controls

- **Left Arrow** - Move left
- **Right Arrow** - Move right
- **Esc** - Quit the game

The AI does not use manual controls but instead relies on its evolved neural network to make movement decisions.

## Project Structure

- `stone_dodge_ai.py`: Main game file where Pygame, NEAT, and the game loop are implemented.
- `assets/`: Contains game assets, including player and rock images, background images, and sound effects.
- `config-feedforward.txt`: NEAT configuration file specifying settings for network architecture, mutation rates, and training parameters.

## Dependencies

- `pygame`: Game engine used to render the game interface and handle sprites.
- `numpy`: Used for numerical computations.
- `neat-python`: Library for implementing neuroevolution through NEAT.

## Configuration

The NEAT configuration is set in `config-feedforward.txt`. Key parameters include:
- `pop_size`: Population size per generation.
- `fitness_threshold`: Required fitness level for training completion.
- `activation_function`: Function to activate nodes in the neural network.

## Contributing

Feel free to open issues or submit pull requests to contribute to this project. 

---

This README outlines the project, how to get started, its dependencies, and how the AI works. Let me know if you’d like any adjustments or further details!
