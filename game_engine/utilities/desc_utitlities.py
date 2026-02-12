import random

from .rng_utilities import random_list_element
chamber_descriptions = [
    "A low stone chamber with damp walls, where the air smells faintly of mold and rust.",
    "Cracked flagstones cover the floor of this room, and water drips steadily from the ceiling above.",
    "An abandoned guard post stands here, marked by a broken spear and a crumbling wooden stool.",
    "This narrow chamber is cluttered with fallen stones, as if part of the ceiling collapsed long ago.",
    "A cold draft moves through this room, causing old cobwebs to sway between the stone pillars.",
    "Faded carvings line the walls, their meaning lost beneath centuries of erosion.",
    "The floor here is slick with moisture, and your footsteps echo sharply in the confined space.",
    "A shallow pool of murky water fills the center of this chamber, reflecting the dim light above.",
    "Rust-stained chains hang from iron hooks along the walls, creaking softly as you pass.",
    "This room smells of old smoke, and blackened scorch marks stain the stone floor.",
    "Broken crates and splintered barrels lie scattered across the chamber, long since looted.",
    "The ceiling arches higher here, giving the chamber an uneasy sense of openness.",
    "Dust coats every surface in this room, disturbed only by your movement through it.",
    "A collapsed doorway blocks one wall, the stones piled in a rough, impassable mound.",
    "This chamber feels strangely quiet, as if sound itself is swallowed by the thick stone walls."
  ]
def chamber_description():
  return random_list_element(chamber_descriptions)
passageways = [
    "A narrow corridor where the walls are damp to the touch and smell of stagnant water.",
    "A long, arched hallway where your footsteps echo with an unsettling metallic ring.",
    "The air grows thin and cold in this passage, lined with jagged, unhewn stone.",
    "Flickering torch brackets remain empty here, casting long, distorted shadows down the path.",
    "A low-ceilinged tunnel that forces taller adventurers to hunch over as they walk.",
    "The floor is covered in a thick layer of dust, undisturbed for decades until now.",
    "A steep stone staircase spirals downward into a thick, clinging mist.",
    "The walls here are etched with faded murals of a civilization long forgotten.",
    "A drafty hallway where the wind whistles through tiny cracks in the masonry.",
    "Sticky, translucent webs hang from the ceiling like tattered curtains.",
    "The scent of ozone and burnt hair lingers in this strangely warm corridor.",
    "A grand gallery supported by crumbling pillars carved in the likeness of weeping giants.",
    "Roots from the surface have broken through the ceiling, dangling like pale veins.",
    "The passage turns at sharp, jagged angles, making it impossible to see far ahead.",
    "A bridge of solid obsidian spans a dark chasm that hums with distant energy.",
    "The floor tiles are loose here, clicking softly under the weight of a footstep.",
    "A claustrophobic crawlspace that smells faintly of wet fur and old copper.",
    "Luminescent fungi cling to the walls, casting a sickly pale green glow on the path.",
    "The masonry is impeccably smooth here, as if melted into place by extreme heat.",
    "A wide hall where the ceiling has partially collapsed, spilling rubble across the floor.",
    "The muffled sound of rhythmic thumping can be heard through the left-hand wall.",
    "A corridor lined with iron-barred alcoves, though whatever they held is long gone.",
    "Water trickles down the walls, collecting in shallow, oily pools on the uneven floor.",
    "The air is thick with the smell of woodsmoke and dried herbs in this section.",
    "A sloping ramp leads deeper into the earth, slick with a thin layer of black moss.",
    "The walls are reinforced with rusted iron plates held by oversized rivets.",
    "A series of small, interconnected chambers that form a winding, labyrinthine path.",
    "Small piles of bleached bones are tucked into the corners of this silent hallway.",
    "The temperature drops sharply, and your breath begins to mist in the stagnant air.",
    "A tunnel carved directly through a vein of dull, reddish quartz.",
    "The ceiling is unnaturally high, disappearing into a darkness no torch can pierce.",
    "Scratches line the walls at chest height, as if something large was dragged through.",
    "A short hall where the floor is composed of decorative, but cracked, marble tiles.",
    "The smell of old parchment and rotting leather wafts from the darkness ahead.",
    "A narrow catwalk overlooking a lower level filled with thick, swirling smoke.",
    "The passage is perfectly circular, resembling the throat of some gargantuan beast.",
    "Clusters of harmless black beetles scurry away from the light of your lanterns.",
    "A hallway where the walls are strangely warm, vibrating with a low frequency.",
    "The path is obstructed by a heavy, tattered velvet curtain smelling of mothballs.",
    "A dead-straight corridor that creates a perfect, terrifying line of sight to the next door."
]
def passageway_descriptions():
  return random_list_element(passageways)

medium_weapons = [
    ("Worn Shortsword", "A practical blade with nicks along its edge, still serviceable despite heavy use."),
    ("Iron Hand Axe", "A solid iron axe with a chipped head and a leather-wrapped handle."),
    ("Balanced Mace", "A blunt weapon with a simple iron head, designed more for durability than elegance."),
    ("Notched Dagger", "A short blade with visible wear, favored for close and desperate fights."),
    ("Rust-Flecked Spear", "A long spear with a sturdy shaft, its metal tip marked by age and use."),
    ("Plain Warhammer", "A heavy hammer built for breaking armor, lacking any decorative detail."),
    ("Broad-Bladed Knife", "A thick, weighty knife meant for combat rather than utility."),
    ("Old Cavalry Saber", "Once well-made, this curved blade has lost some of its former sharpness."),
    ("Steel Club", "A reinforced club with metal bands bolted into its wooden frame."),
    ("Guard’s Longsword", "A regulation weapon bearing scratches from many previous engagements.")
]

good_weapons = [
    ("Well-Forged Longsword", "A carefully balanced blade that holds its edge remarkably well."),
    ("Tempered Battle Axe", "Its sharpened edge and reinforced haft suggest skilled craftsmanship."),
    ("Knight’s Mace", "A polished iron head mounted on a firm grip, capable of crushing armor."),
    ("Fine Steel Dagger", "Lightweight and razor-sharp, designed for precision strikes."),
    ("Heavy War Pick", "A hardened point meant to pierce even reinforced plating."),
    ("Masterwork Spear", "A long, flexible shaft topped with a finely honed steel tip."),
    ("Engraved Shortsword", "Subtle engravings run along the blade, hinting at pride in its creation."),
    ("Balanced Flail", "A well-made chain and striking head that move smoothly in practiced hands."),
    ("Steel Morningstar", "Evenly weighted and brutally effective, with no wasted material."),
    ("Veteran’s Blade", "A trusted weapon that shows signs of care rather than neglect.")
]
def weapon_description(rarity):
  if rarity < 5:
    return random_list_element(medium_weapons)
  else:
    return random_list_element(good_weapons)
  
medium_armor = [
    ("Chainmail Shirt", "Interlocking rings provide solid protection without excessive weight."),
    ("Reinforced Leather Armor", "Thick leather plates sewn together to absorb glancing blows."),
    ("Iron Breastplate", "A solid chest piece bearing dents from previous battles."),
    ("Scale Armor Vest", "Overlapping metal scales stitched onto a leather backing."),
    ("Guard Helm", "A simple iron helmet designed for practicality over comfort."),
    ("Padded Gambeson", "Layers of quilted cloth offering modest protection and warmth."),
    ("Steel Greaves", "Leg armor with worn straps but intact metal plating."),
    ("Brigandine Coat", "Metal plates hidden beneath heavy fabric, flexible but durable."),
    ("Round Shield", "A wooden shield reinforced with iron bands along its rim."),
    ("Iron Pauldrons", "Shoulder plates that restrict movement slightly but offer reliable defense.")
]
good_armor = [
    ("Polished Breastplate", "A carefully shaped steel breastplate that reflects light and resists heavy blows."),
    ("Knight’s Chainmail", "Tightly linked rings forged from quality steel, offering excellent protection and flexibility."),
    ("Hardened Leather Armor", "Thick, treated leather reinforced at key points for improved durability."),
    ("Tempered Steel Helm", "A well-fitted helmet that protects the head without severely limiting vision."),
    ("Reinforced Brigandine", "Hidden steel plates beneath heavy fabric provide strong defense with mobility."),
    ("Steel Greaves and Vambraces", "Matching limb guards crafted to distribute impact evenly."),
    ("Heater Shield", "A well-balanced shield with reinforced edges and a sturdy central boss."),
    ("Officer’s Half-Plate", "Partial plate armor designed for leaders who value both protection and command presence."),
    ("Articulated Pauldrons", "Carefully jointed shoulder armor that moves smoothly with the wearer."),
    ("Veteran’s Armor Coat", "Armor that shows signs of expert maintenance rather than battlefield neglect.")
]

def armor_description(rarity):
  if rarity < 5:
    return random_list_element(medium_armor)
  else:
    return random_list_element(good_armor)

mystery_potions = [
    ("Clouded Vial", "A murky liquid swirls inside, shifting color when shaken."),
    ("Cracked Glass Flask", "The contents glow faintly, though its purpose is unclear."),
    ("Sealed Alchemical Bottle", "No label marks this potion, and the liquid inside is unsettlingly still.")
]
def potion_description():
  return random_list_element(mystery_potions)

low_trinkets = [
    ("Bent Copper Ring", "A misshapen ring with little value beyond sentiment."),
    ("Cracked Clay Charm", "A small token that may once have been worn for luck."),
    ("Tarnished Locket", "The hinge barely holds, and the image inside has faded away."),
    ("Wooden Dice Set", "Roughly carved and uneven, likely used for idle gambling."),
    ("Frayed Cloth Talisman", "A strip of fabric tied with string, its meaning long forgotten.")
]

high_trinkets = [
    ("Silver Inlaid Brooch", "Carefully crafted, its design suggests noble ownership."),
    ("Gem-Set Ring", "A polished stone sits firmly in a well-made metal band."),
    ("Engraved Pocket Relic", "Covered in precise markings, possibly of religious origin."),
    ("Gold Filigree Pendant", "Delicate metalwork forms an intricate and valuable piece."),
    ("Jeweled Dice Pair", "Finely balanced and adorned, more status symbol than game piece.")
]

def base_item_description(rarity):
  if rarity < 5:
    return random_list_element(high_trinkets)
  else:
    return random_list_element(low_trinkets)

dungeon_enemies = [
    ("Hollow-Eyed Cultist", "A mortal servant to dark forces, whispering prayers and clutching a ritual blade."),
    ("Rust-Eaten Animated Armor", "An empty suit of plate that clatters with each step, driven by magic alone."),
    ("Crypt Spider", "A chitinous predator the size of a hound, its eyes glimmering in the dark like ink-black pearls."),
    ("Ooze Spawn", "A wobbling glob of corrosive slime that absorbs weapons, light, and anything foolish enough to touch it."),
    ("Plague-Scarred Bat", "A huge bat with patchy fur and cracked skin, shrieking as it wheels through stagnant air."),
    ("Skeleton Footman", "Animated bones clad in rusted armor, attacking with the fading memory of drill and discipline."),
    ("Carrion Crawler", "A pale, many-legged creature that drags its slimy bulk across the floor, seeking paralyzed prey."),
    ("Giant Rat", "Vermin the size of dogs, often swarming and spreading disease."),
    ("Giant Spider", "Web-weaving predator with venomous fangs and cunning ambush tactics."),
    ("Rotting Ghoul", "A corpse animated by hunger, its eyes alert and unfocused as it sniffs out the living."),
    ("Dungeon Rat Swarm", "A churning mass of oversized rats, their teeth clicking as they surge forward in a tide."),
    ("Skeleton Warrior", "Reanimated bones clad in rusted armor, driven by dark will."),
    ("Animated Suit of Armor", "Hollow plate mail brought to life by magic, relentless and unfeeling."),
    ("Kobold", "Small reptilian humanoid with a knack for traps and cowardly tactics."),
    ("Deep Gnome", "Clever subterranean dweller skilled in stealth and illusion magic."),
    ("Grimlock", "Blind, brutish humanoid with an acute sense of smell and aggression."),
    ("Troglodyte", "Primitive reptilian humanoid, reeks of musk and savagery."),
    ("Goblin Scout", "Fast and elusive scout, often the eyes and ears of larger goblin warbands."),
    ("Cave Stalker", "A lanky, grey-skinned thing that clings to stone walls and drops silently on its prey."),
    ("Gravebound Spirit", "A flickering phantom bound to the place of its death, drifting in looping patterns of memory."),
    ("Tunnel Kobold Sapper", "A scrawny trap-maker carrying unstable explosives and too much confidence."),
    ("Mire Troll", "A hulking brute caked in filth, regenerating flesh as fast as weapons carve it away."),
    ("Spectre", "Ghostly apparition that drains warmth and life from nearby souls."),
    ("Wight", "Undead warrior with cursed strength and a hunger for the living."),
    ("Ogre", "Massive, dim-witted brute with a club that can shatter stone."),
    ("Cave Troll", "Thick-skinned giant dwelling in caves, extremely strong and territorial."),
    ("Stone Golem", "Magical construct of immense weight and force, nearly impervious to blades."),
    ("Mummy", "Wrapped in ancient linens, cursed to protect tombs with dark magic."),
    ("Pit Crawler", "Sinister, skittering horror that burrows through walls and flesh alike."),
    ("Bone Naga", "Serpentine undead with spellcasting power and a gaze that chills the spine."),
    ("Land Shark", "Massive beast with armored hide and a hunger for anything that moves underground."),
    ("Death Knight", "Fallen champion clad in blackened armor, wielding unholy powers and blades."),
    ("Drake", "Wingless draconic creature with elemental breath and raw fury."),
    ("Hydra", "Many-headed serpent beast; cut one head off, two may take its place."),
    ("Chimera", "Three-headed monstrosity that breathes fire, roars thunder, and strikes with venom."),
    ("Wyvern", "Flying reptile with a venomous stinger and a taste for meat."),
    ("Purple Worm", "Titanic worm with a gaping maw, capable of devouring adventurers whole.")
]

def enemy_description(cr):
  list_length = len(dungeon_enemies)
  # We divide the list into 5 roughly equal chunks
  chunk_size = list_length // 5
  
  # Calculate the start and end indices for the slice
  # CR 1 -> 0 to chunk_size
  # CR 5 -> (4 * chunk_size) to the end of the list
  start_index = (cr - 1) * chunk_size
  
  # For the final CR level, we go to the very end to catch any remainder
  if cr == 5:
      monster_pool = dungeon_enemies[start_index:]
  else:
      end_index = start_index + chunk_size
      monster_pool = dungeon_enemies[start_index:end_index]
  return random.choice(monster_pool)
dungeon_traps = [
    ("Fire Bomb", "A hidden pressure plate ignites an explosive canister.", "dex"),
    ("Wall Arrows", "Mechanical sensors trigger a volley of poison-tipped arrows.", "dex"),
    ("Poison Gas", "A hollow floor tile releases a cloud of toxic emerald vapors.", "con"),
    ("Spike Pit", "A section of the floor hinges open to reveal a 20ft drop.", "dex"),
    ("Rolling Ball", "A massive stone sphere is released from the ceiling.", "dex"),
    ("Crushing Ceiling", "The exit doors lock as the ceiling slowly descends.", "dex"),
    ("Electric Floor", "Metal floor plates become electrified, stunning the victim.", "con"),
    ("Spectral Scythe", "An enchanted blade swings from a hidden groove.", "wis"),
    ("Teleportation Loop", "A shimmering rune that teleports the victim back to the start.", "cha"),
    ("Acid Spray", "Vents in the masonry spray a fine mist of corrosive acid.", "con"),
    ("Siren's Mirror", "A cursed glass that compels the viewer to walk toward it.", "cha"),
    ("Hidden Tripwire", "A thin wire nearly invisible to the naked eye.", "wis")
]
def trap_description():
  return random_list_element(dungeon_traps)
# Format: (Player Choice 1, Player Choice 2, Response to 1, Response to 2)
dialogue_tree = [
    (
        "I've come to save the village.", 
        "I'm just here for the gold.", 
        "A hero! We haven't seen one of those since the Great Frost.", 
        "At least you're honest. The coins are in the chest, if you survive."
    ),
    (
        "Is there a faster way through the mountains?", 
        "Are the mountain passes safe?", 
        "Only if you fancy a climb through the Devil's Chimney.", 
        "Safe? Only if you consider a pack of hungry wolves 'safe'."
    ),
    (
        "Lower your weapon, I mean no harm.", 
        "Drop the sword before I make you.", 
        "Easy there... my nerves are a bit frayed lately.", 
        "Big words for someone standing in range of my blade!"
    ),
    (
        "Tell me about the wizard in the tower.", 
        "I heard the wizard is a fraud.", 
        "He's brilliant, but he hasn't been seen since the lightning hit.", 
        "Careful! He has ears everywhere... and some of them aren't even his."
    )
]
dungeon_npcs = [
    (
        "The Skeletal Archivist", "An ancient undead librarian who refuses to pass on until every scroll in the dungeon is properly cataloged."
    ),
    (
        "Fizzlebang the 'Exterminator'", "A frantic goblin alchemist looking for 'volunteer' testers for his highly unstable monster-repelling potions."
    ),
    (
        "The Cursed Statue", "A stone guardian that can only speak in riddles and offers cryptic directions in exchange for a drop of blood."
    ),
    (
        "Barnaby the Mimic-Slayer", "A grizzled, paranoid veteran who spends his time stabbing every chest, chair, and door handle he encounters."
    ),
    (
        "The Lost Squire", "A terrified youth hiding in a barrel, hoping someone will lead them back to the surface before their torch burns out."
    ),
    (
        "Wraith of the Vault", "A shimmering spirit that offers to open locked doors if you can tell it a story from the world of the living."
    ),
    (
        "Grog the Gourmet", "An ogre wearing a stained chef's hat, obsessed with finding the 'perfect spice' found only on Giant Spider legs."
    ),
    (
        "The Shadow Merchant", "A hooded figure who only appears in the darkest corners, trading high-tier loot for the player's most cherished memories."
    )
]
def npc_description():
  return random_list_element(dungeon_npcs)

def npc_dialogue():
  return random_list_element(dialogue_tree)