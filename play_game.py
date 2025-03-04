from copy import deepcopy

from move import SlideDown, SlideLeft, SlideRight, SlideUp

class PlayGame():
    def __init__(self, initial_state, optimal_moves):
        self.initial_state = initial_state
        self.optimal_moves = optimal_moves
        self.running = False
        self.move_history = []
        self.running = True
    def play_game(self):
        print("Initial board:")
        print(self.initial_state)
        i = 0
        while self.running:
            print("")
            user_input = input("Enter move (right, left, up, down, hint, quit): ").strip().lower()
            if user_input in ["right", "left", "up", "down"]:
                if user_input == "up":
                    next_state = SlideUp().apply(self.initial_state)
                    if next_state:
                        self.initial_state = next_state
                        i += 1
                elif user_input == "down":
                    next_state = SlideDown().apply(self.initial_state)
                    if next_state:
                        self.initial_state = next_state
                        i += 1
                elif user_input == "left":
                    next_state = SlideLeft().apply(self.initial_state)
                    if next_state:
                        self.initial_state = next_state
                        i += 1
                elif user_input == "right":
                    next_state = SlideRight().apply(self.initial_state)
                    if next_state:
                        self.initial_state = next_state
                        i += 1
                else:
                    print("Invalid move. Please try again.")

                print("Number of moves: ", i)
                print("New board:")
                print(self.initial_state)

                if self.initial_state.is_solved():
                    print("You won!")
                    if i == self.optimal_moves:
                        print(f"Congratulations! You have achieved the perfect score: {i} moves.")
                    else:
                        print("Congratulations! Solution found in", i, "moves.")
                        print("The perfect score is", self.optimal_moves, "moves.")
                    break

            elif user_input == "hint":
                if self.get_hint():
                    print("Hint: ", self.get_hint())
                else:
                    print("No solution found.")

            elif user_input == "quit":
                print("Exiting game...")
                self.running = False
            else:
                print("Invalid input. Please enter 'right', 'left', 'up', 'down', or 'quit'.")



    def get_hint(self):
        return self.bfs()

    def bfs(self):
            problem = deepcopy(self.initial_state)
            queue = [(problem, [])]
            visited_hashes = set()
            visited_hashes.add(hash(problem))

            while queue:
                current_state, path = queue.pop(0)

                if current_state.is_solved():
                    return path[0]

                for move in [SlideLeft(), SlideRight(), SlideUp(), SlideDown()]:
                    next_state = move.apply(current_state)
                    if next_state:
                        next_state_hash = hash(next_state)
                        if next_state_hash not in visited_hashes:
                            visited_hashes.add(next_state_hash)
                            queue.append((next_state, path + [type(move).__name__]))

            return None