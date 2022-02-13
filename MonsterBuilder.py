import pandas
import sys

stat_table = pandas.read_csv("MonsterBuilderTable.csv",index_col=0)

Tier = str(sys.argv[1])
Org = str(sys.argv[2])

class Monster:
	def __init__(self,tier,org):
		self.tier = tier
		self.org = org
		self.stats = {"AC":"Average","HP":"Average","Offence":"Average","Dmg":"Average"}
	
	def __str__(self):
		return "AC:{AC} HP:{HP}\n\
Att:{Att} Dmg:{Dmg}\n\
Save DC:{SvDC}\n\
".format(
AC=stat_table.loc["AC"][f'{self.tier}_{self.stats["AC"]}'],
HP=stat_table.loc[f"Hp{Org}"][f'{self.tier}_{self.stats["HP"]}'],
Att=stat_table.loc["Attack"][f'{self.tier}_{self.stats["Offence"]}'],
SvDC=stat_table.loc["SaveDC"][f'{self.tier}_{self.stats["Offence"]}'],
Dmg=stat_table.loc[f"Dmg{Org}"][f'{self.tier}_{self.stats["Dmg"]}'])


class Brute(Monster):
	def __init__(self,tier,org):
		super(Brute,self).__init__(tier,org)
		self.stats["HP"] = "Good"
		self.stats["Dmg"] = "Good"
		self.stats["Offence"] = "Poor"
		self.stats["AC"] = "Poor"

class Artillery(Monster):
	def __init__(self,tier,org):
		super(Artillery,self).__init__(tier,org)
		self.stats["Dmg"] = "Good"
		self.stats["AC"] = "Poor"

class Soldier(Monster):
	def __init__(self,tier,org):
		super(Soldier,self).__init__(tier,org)
		self.stats["AC"] = "Good"
		self.stats["Dmg"] = "Poor"
	
class Controler(Monster):
	def __init__(self,tier,org):
		super(Controler,self).__init__(tier,org)
		self.stats["Off"] = "Good"
		self.stats["HP"] = "Poor"

	
class Lurker(Monster):
	def __init__(self,tier,org):
		super(Lurker,self).__init__(tier,org)
		self.stats["HP"] = "Poor"
		self.stats["AC"] = "Poor"
		self.stats["Dmg"] = "Good"
		self.stats["Offence"] = "Good"
	
class Skirmisher(Monster):
	def __init__(self,tier,org):
		super(Skirmisher,self).__init__(tier,org)
		self.stats["AC"] = "Good"
		self.stats["HP"] = "Good"

		
print(str(Controler(Tier,Org)))
