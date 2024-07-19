import random
import matplotlib.pyplot as plt
import pandas as pd

# Card and deck definitions
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Deck:
    def __init__(self):
        self.deck = [rank + ' of ' + suit for suit in suits for rank in ranks]
        random.shuffle(self.deck)
    
    def deal_card(self):
        return self.deck.pop()
    
    def reset_deck(self):
        self.__init__()

# Function to calculate the value of a hand
def calculate_hand_value(hand):
    value = sum(values[card.split(' ')[0]] for card in hand)
    aces = sum(card.startswith('A') for card in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Function to simulate a single hand of blackjack
def play_hand(deck):
    player_hand = [deck.deal_card(), deck.deal_card()]
    dealer_hand = [deck.deal_card(), deck.deal_card()]

    # Player's turn
    while calculate_hand_value(player_hand) < 17:
        player_hand.append(deck.deal_card())

    # Dealer's turn
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.deal_card())

    return player_hand, dealer_hand

# Function to determine the result of a hand
def determine_winner(player_hand, dealer_hand):
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    
    if player_value > 21:
        return 'loss'
    elif dealer_value > 21 or player_value > dealer_value:
        return 'win'
    elif player_value < dealer_value:
        return 'loss'
    else:
        return 'push'

# Function to simulate multiple hands and collect statistics
def simulate_blackjack(n_hands, initial_bankroll=1000):
    deck = Deck()
    results = {'win': 0, 'loss': 0, 'push': 0}
    player_bank = initial_bankroll
    bankroll_history = [initial_bankroll]

    for i in range(n_hands):
        bet = player_bank * 0.02  # Bet 2% of bankroll
        
        if bet <= 10:  # End game if player runs out of money
            break
        
        if len(deck.deck) < 20:  # Reset deck if not enough cards
            deck.reset_deck()
        
        player_hand, dealer_hand = play_hand(deck)
        result = determine_winner(player_hand, dealer_hand)
        results[result] += 1

        if result == 'win':
            player_bank += bet
        elif result == 'loss':
            player_bank -= bet

        bankroll_history.append(player_bank)  # Update bankroll history
        
        if player_bank <= 0:  # End game if player runs out of money
            break

    return results, player_bank, bankroll_history, i+1  # Return the number of hands played

# Function to display statistics
def display_statistics(results, player_bank, bankroll_history):
    print(f"Final bank amount: ${player_bank}")
    print(f"Wins: {results['win']}")
    print(f"Losses: {results['loss']}")
    print(f"Pushes: {results['push']}")
    
    # Visualizing results
    df = pd.DataFrame(list(results.items()), columns=['Result', 'Count'])
    df.set_index('Result', inplace=True)
    df.plot(kind='bar', legend=False)
    plt.title('Blackjack Results')
    plt.ylabel('Count')
    plt.show()

    # Visualizing bankroll over time
    plt.plot(bankroll_history)
    plt.title('Bankroll Over Time')
    plt.xlabel('Hand Number')
    plt.ylabel('Bankroll')
    plt.show()

# Main function
def main():
    n_hands = 10000  # Number of hands to simulate
    n_generations = 100  # Number of generations to simulate
    initial_bankroll = 1000  # Initial bankroll

    best_bankroll = -float('inf')
    worst_bankroll = float('inf')
    best_hands = -1
    worst_hands = -1

    for i in range(n_generations):
        results, player_bank, bankroll_history, hands_played = simulate_blackjack(n_hands)  # Get number of hands played

        if player_bank > best_bankroll or (player_bank == best_bankroll and hands_played > best_hands):
            best_bankroll = player_bank
            best_history = bankroll_history
            best_hands = hands_played

        if player_bank < worst_bankroll or (player_bank == worst_bankroll and hands_played < worst_hands):
            worst_bankroll = player_bank
            worst_history = bankroll_history
            worst_hands = hands_played


        # Plot each generation with a certain transparency
        plt.plot(bankroll_history, alpha=0.1, color='gray')

    # Draw a horizontal line at the initial bankroll
    plt.axhline(y=initial_bankroll, color='blue', linestyle='--')

    # Display best and worst bankroll histories
    plt.plot(best_history, label='Best', color='green')
    plt.plot(worst_history, label='Worst', color='red')
    plt.title('Bankroll Over Time')
    plt.xlabel('Hand Number')
    plt.ylabel('Bankroll')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()