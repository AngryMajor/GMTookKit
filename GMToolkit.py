import discord

TOKEN = None

with open('Bot_token.txt') as f: 
	TOKEN = f.readlines()[0]

client = discord.Client()

command_handeler = None

@client.event
async def on_ready():
	print("Booting up!")
	
@client.event
async def on_message(message):	
	username = str(message.author).split('#')[0]
	message_text = str(message.content).lower()
	channel  = str(message.channel.name)
	
	if message.author == client.user:
		return
	
	if channel == "combat":
		argvs = message_text.split(' ')
		return_string = command_handeler.process_command(argvs)
		
		if return_string != None:
			await message.channel.send(return_string)

class CommandHandeler:
	def __init__(self):
		self.command_palet = {}

	def process_command(self, argvs):
		if(argvs[0] in self.command_palet): 
			return self.command_palet[argvs[0]].process(argvs[1:])
		else: return None

class InitRunner:
	def __init__(self, _init_order_list_list=list()):
		self._init_order_list = _init_order_list_list
		self._curr_combatant = None
			
	
	def process(self, argvs):
		sub_command = argvs[0]
		if(sub_command == "add"): return self._add_combatant(argvs[1:])
		elif(sub_command == "remove"): return self._remove_combatant(argvs[1:])
		elif(sub_command == "show"): return str(self._init_order_list)
		elif(sub_command == "n" or sub_command == "next"): return self._next_combatant(argvs[1:])
		elif(sub_command == "b" or sub_command == "back"): return self._privious_combatant(argvs[1:])
		elif(sub_command == "end"): return self._end_inititive(argvs[1:])
	
	def _add_combatant(self,argvs):
		init_tuple = (argvs[0],int(argvs[1]))
		
		if init_tuple in self._init_order_list:
			return "Duplicates Not Allowed"
		
		self._init_order_list.append(init_tuple)
		self._init_order_list.sort(key= lambda item : item[1], reverse=True)
		return "**{}** added at {}".format(init_tuple[0],init_tuple[1])
		
	def _remove_combatant(self,argvs):
		name_for_removal = argvs[0]
		matches = [item for item in self._init_order_list if item[0] == name_for_removal]
		
		if len(matches) == 0:
			return "**{}** not found".format(name_for_removal) 
				
		if self._curr_combatant != None and self._curr_combatant[0] == name_for_removal:
			self._move_curr_combatent_off_removal_target(matches,name_for_removal)
					
		for match in matches:
			self._init_order_list.remove(match)
		return "**{}** removed".format(name_for_removal)
		
	def _move_curr_combatent_off_removal_target(self,removal_matches,name_for_removal):
		if self._curr_combatant != None and self._curr_combatant[0] != name_for_removal:
			return
				
		if len(self._init_order_list) == len(removal_matches):#i.e. same list
			self._curr_combatant = None
			return
		
		while self._curr_combatant[0] == name_for_removal:
			self._next_combatant([])
	
	def _next_combatant(self,argvs):
		init_order_size = len(self._init_order_list)
		
		if init_order_size == 0:
			return "No Combatants Entered"
		
		curr_combatent_rank = None
		if self._curr_combatant == None:
			self._curr_combatant = self._init_order_list[0]
			curr_combatent_rank = 0
		else:
			curr_combatent_rank = self._init_order_list.index(self._curr_combatant)
			curr_combatent_rank += 1
			self._curr_combatant = self._init_order_list[(curr_combatent_rank) % init_order_size]
			
		if(init_order_size > 1):
			on_deck_combatent = self._init_order_list[(curr_combatent_rank +1) % init_order_size]
			return "It's **{}** turn, On Deck is **{}**".format(self._curr_combatant[0],on_deck_combatent[0])
		else:
			return "It's **{}** turn".format(self._curr_combatant[0])

		
	def _privious_combatant(self,argvs):
		init_order_size = len(self._init_order_list)
		
		if init_order_size == 0:
			return "No Combatants Entered"
		
		if self._curr_combatant == None:
			self._curr_combatant = self._init_order_list[init_order_size-1]
		else:
			curr_combatent_rank = self._init_order_list.index(self._curr_combatant)
			self._curr_combatant = self._init_order_list[(curr_combatent_rank -1) % init_order_size]
		return str(self._curr_combatant)
		
	def _end_inititive(self,argvs):
		self._init_order_list.clear()
		self._curr_combatant = None
		return "--- **Initive over** ---"




if __name__ == "__main__":
	client.run(TOKEN)
	command_handeler = CommandHandeler()
	init_runner = InitRunner(command_handeler)
	command_handler.command_palet["i"] = init_runner
	command_handler.command_palet["init"] = init_runner
	command_handler.command_palet["initiative"] = init_runner
