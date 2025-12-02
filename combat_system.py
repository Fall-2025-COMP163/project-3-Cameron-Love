"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Cameron Love

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    
    #Creates all enemys
    enemy_types = {
        
        # Goblin - Weakest enemy
        "goblin": {
            "name": "Goblin",
            "health": 80,       # Buffed from 50
            "strength": 10,     # Buffed from 8
            "magic": 2,
            "xp_reward": 35,
            "gold_reward": 15
        },
        
        # Orc - Average enemy
        "orc": {
            "name": "Orc",
            "health": 150,      # Buffed from 80
            "strength": 20,     # Buffed from 12
            "magic": 5,
            "xp_reward": 80,
            "gold_reward": 40
        },
        
        # New Enemy (Creativity Bonus) 
        "vampire": {
            "name": "Vampire",
            "health": 120,
            "strength": 15,
            "magic": 30,       
            "xp_reward": 120,
            "gold_reward": 60
        },

        # Dragon - The Boss
        "dragon": {
            "name": "Dragon",
            "health": 500,      # Massive buff from 200
            "strength": 45,     # Buffed from 25
            "magic": 20,
            "xp_reward": 500,
            "gold_reward": 300
        }
    }
    if enemy_type not in enemy_types:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    
    base = enemy_types[enemy_type]

    #Assigns the enemys stats based on its class
    enemy = {
        "name": base["name"],
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "xp_reward": base["xp_reward"],
        "gold_reward": base["gold_reward"]
    }
    return enemy


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    
    #Assigns enemies based on character level
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    return create_enemy(enemy_type)


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy

        self.combat_active = True

        self.turn_number = 1

        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        
        
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        
        #You cant start battle if your character is dead
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight")
        
        #Loop goes until the battle ends
        while self.combat_active:

            self.player_turn()
            result = self.check_battle_end()
            if not self.combat_active:
                break
            if result:
                break

            #Enimies turn
            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                break

            #Increment turn counter
            self.turn_number += 1

        #Determines the winner and rewards after loop ends
        if result == "player":
            rewards = get_victory_rewards(self.enemy)

            #Award XP and gold to character
            #XP leveling happens in character manager
            self.character["experience"] += rewards["xp"]
            self.character["gold"] += rewards["gold"]

            return {
                'winner': 'player',
                'xp_gained': rewards["xp"],
                'gold_gained': rewards["gold"]
            }
        
        elif result == "enemy":
            return {
                'winner': 'enemy',
                'xp_gained': 0,
                'gold_gained': 0
            }
        
        else:
            #Escape means no winner
            return {
                'winner': 'none',
                'xp_gained': 0,
                'gold_gained': 0
            }
        
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        
        #Checks if a battle is in progress
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active")
        
        #Displays stats
        display_combat_stats(self.character, self.enemy)

        #Shows your Options
        print("\nYour Turn! Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        #User picks their choice
        choice = input("Enter choice (1-3): ").strip()

        #Basic Attack
        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")

        #Special Ability
        elif choice == "2":
            result_text = use_special_ability(self.character, self.enemy)
            display_battle_log(result_text)

        #Try to Run
        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You successfully escaped the battle!")
            else:
                display_battle_log("Escape failed! The battle continues.")
                return  # End turn if escape fails
        else:
            display_battle_log("Invalid choice! You lose your turn.")



    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        
        #Checks if a battle is in progress
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active")
        
        #The enemy attacks the player
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)

        #Logs the attack
        display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage!")

    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        
        #Calculates damage from attack
        damage = attacker["strength"] - (defender["strength"] // 4)


        #Makes sure minimum damage of 1
        if damage < 1:
            damage = 1

        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        
        #Reduces health by damage
        target["health"] -= damage

        #Prevent negative health
        if target["health"] < 0:
            target["health"] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        
        #If the enemy dies that means player wins
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        
        #If the character dies that means enemy wins
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        
        #The battle is still ongoing
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        
        import random
        success = random.randint(0, 1)  # 0 = fail, 1 = success

        if success == 1:
            self.combat_active = False
            return True
    
        return False


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    
    class_type = character["class"]

    if class_type == "Warrior":
        return warrior_power_strike(character, enemy)

    elif class_type == "Mage":
        return mage_fireball(character, enemy)

    elif class_type == "Rogue":
        return rogue_critical_strike(character, enemy)

    elif class_type == "Cleric":
        return cleric_heal(character)

    else:
        raise InvalidTargetError("Unknown character class for ability.")



def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    #Regular damage calculation
    base_damage = character["strength"] - (enemy["strength"] // 4)

    #Minimum damage of 1
    if base_damage < 1:
        base_damage = 1

    #Doubles the damage for power strike
    final_damage = base_damage * 2

    #Applys the  damage to enemy
    enemy["health"] -= final_damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"You use Power Strike and deal {final_damage} damage to the {enemy['name']}!"


    # TODO: Implement power strike
    # Double strength damage
    

def mage_fireball(character, enemy):
    """Mage special ability"""

    #Regular magic damage calculation
    base_damage = character["magic"]

    #Fireball doubles the magic damage
    final_damage = base_damage * 2

    #Applys damage to enemy
    enemy["health"] -= final_damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"You cast Fireball and deal {final_damage} magic damage to the {enemy['name']}!"

    # TODO: Implement fireball
    # Double magic damage
    

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    
    import random
        # Calculate base damage (same formula as normal attack)
    base_damage = character["strength"] - (enemy["strength"] // 4)

    if base_damage < 1:
        base_damage = 1

    # 50% chance for a critical hit
    crit = random.randint(0, 1)  # 0 = normal, 1 = critical

    if crit == 1:
        final_damage = base_damage * 3
        crit_text = "Critical Strike!"
    else:
        final_damage = base_damage
        crit_text = "You strike swiftly."

    # Applys damage
    enemy["health"] -= final_damage
    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"{crit_text} You dealt {final_damage} damage!"
    # TODO: Implement critical strike
    # 50% chance for triple damage

def cleric_heal(character):
    """Cleric special ability"""
    heal_amount = 30

    # Calculates how much healing can actually be applied
    max_hp = character["max_health"]
    current_hp = character["health"]

    new_hp = current_hp + heal_amount

    # Cap at max health
    if new_hp > max_hp:
        new_hp = max_hp

    actual_healed = new_hp - current_hp

    # Applys healing
    character["health"] = new_hp

    return f"You pray for divine aid and heal {actual_healed} HP!"
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return character["health"] > 0


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }



def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

