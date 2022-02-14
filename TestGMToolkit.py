import unittest
import GMToolkit as gmt

class TestCommandHandler(unittest.TestCase):
	class TestCommand:
			def __init__(self):
				self.called = False
			def process(self, argvs):
				self.called = True
		
	def test_process_command(self):		
		test_command_obj = self.TestCommand()	
		
		command_handler = gmt.CommandHandeler()
		command_handler.command_palet["test"] = test_command_obj
		command_handler.process_command(["test"])
		
		self.assertTrue(test_command_obj.called)
		
	def test_fail_process_command(self):		
		test_command_obj = self.TestCommand()	
		
		command_handler = gmt.CommandHandeler()
		command_handler.command_palet["test"] = test_command_obj
		command_handler.process_command(["not_test"])
		self.assertTrue(test_command_obj.called == False)
		
	
class TestInitRunner(unittest.TestCase):
	def setUp(self):
		self.init_order_list = list()
		self.target = gmt.InitRunner(self.init_order_list)

	def test_show_empty(self):
		self.assertEqual(self.target.process(["show"]),"[]")
		
	def test_add_item(self):
		self.target.process(["add","item","1"])
		self.assertEqual(self.target.process(["show"]),"[('item', 1)]")
		
		self.target.process(["add","item2","2"])
		self.assertEqual(self.target.process(["show"]),"[('item2', 2), ('item', 1)]")
	
	def test_add_item_duplicate(self):
		self.target.process(["add","item","1"])
		self.assertEqual(self.target.process(["show"]),"[('item', 1)]")
		
		self.target.process(["add","item","1"])
		self.assertEqual(self.target.process(["show"]),"[('item', 1)]")
		
		self.target.process(["add","item","2"])
		self.assertEqual(self.target.process(["show"]),"[('item', 2), ('item', 1)]")
	
	def test_remove_item(self):
		self.init_order_list.append(("item",1))
		self.init_order_list.append(("item2",2))

		self.target.process(["remove","item2"])
		self.assertEqual(self.target.process(["show"]),"[('item', 1)]")
		
		self.target.process(["remove","item"])
		self.assertEqual(self.target.process(["show"]),"[]")
	
	def test_remove_item_not_found(self):
		self.assertEqual(self.target.process(["remove","item"]),"**item** not found")
		
	def test_remove_tiem_multipul_found(self):
		self.init_order_list.append(("item",1))
		self.init_order_list.append(("item",2))

		self.assertEqual(len(self.init_order_list),2)
		self.target.process(["remove","item"])
		self.assertEqual(len(self.init_order_list),0)

	def test_remove_item_only_item_in_list(self):
		self.init_order_list.append(("item",1))
		self.init_order_list.append(("item",2))
		
		self.target.process(["remove","item"])
		
		self.assertEqual(self.target.process(["next"]),"No Combatants Entered")

		
	def test_remove_curr_combatent(self):
		self.target.process(["add","item","1"])
		self.target.process(["add","item2","2"])	

		self.assertEqual(self.target.process(["next"]),"It's **item2** turn, On Deck is **item**")
		self.target.process(["remove","item2"])
		self.assertEqual(self.target.process(["next"]),"It's **item** turn")
		
		self.target.process(["remove","item"])
		self.assertEqual(self.target.process(["next"]),"No Combatants Entered")
	
	def test_next_successive_adding(self):
		self.assertEqual(self.target.process(["next"]),"No Combatants Entered")
		
		self.init_order_list.append(("item",1))		
		self.assertEqual(self.target.process(["next"]),"It's **item** turn")
		
		self.init_order_list.append(("item2",2))		
		self.assertEqual(self.target.process(["next"]),"It's **item2** turn, On Deck is **item**")
		
		self.init_order_list.append(("item3",5))		
		self.assertEqual(self.target.process(["next"]),"It's **item3** turn, On Deck is **item**")

	def test_next_correct_order(self):
		self.target.process(["add","item","1"])
		self.target.process(["add","item3","3"])
		self.target.process(["add","item2","2"])
	
		self.assertEqual(self.target.process(["next"]),"It's **item3** turn, On Deck is **item2**")
		self.assertEqual(self.target.process(["next"]),"It's **item2** turn, On Deck is **item**")
		self.assertEqual(self.target.process(["next"]),"It's **item** turn, On Deck is **item3**")


	def test_previus_successive_adding(self):
		self.assertEqual(self.target.process(["back"]),"No Combatants Entered")
		
		self.init_order_list.append(("item",1))		
		self.assertEqual(self.target.process(["back"]),"('item', 1)")
		
		self.init_order_list.append(("item2",2))		
		self.assertEqual(self.target.process(["back"]),"('item2', 2)")
		
		self.init_order_list.append(("item3",3))		
		self.assertEqual(self.target.process(["back"]),"('item', 1)")

	def test_previus_correct_order(self):
		self.target.process(["add","item","1"])
		self.target.process(["add","item2","2"])
		self.target.process(["add","item3","3"])
	
		self.assertEqual(self.target.process(["back"]),"('item', 1)")
		self.assertEqual(self.target.process(["back"]),"('item2', 2)")
		self.assertEqual(self.target.process(["back"]),"('item3', 3)")

	def test_end(self):
		self.init_order_list.append(("item",1))		
		self.assertEqual(len(self.init_order_list),1)

		self.target.process(["end"])
		
		self.assertEqual(len(self.init_order_list),0)
	
	def test_remove_curr_combatent(self):
		self.target.process(["add","item","1"])
		self.target.process(["add","item2","2"])	

		self.assertEqual(self.target.process(["next"]),"It's **item2** turn, On Deck is **item**")
		self.target.process(["remove","item2"])
		self.assertEqual(self.target.process(["next"]),"It's **item** turn")
		
		self.target.process(["remove","item"])
		self.assertEqual(self.target.process(["next"]),"No Combatants Entered")

class TestDMGTracker(unittest.TestCase):
	
	def setUp(self):
		self.target = gmt.DMGTracker()
	
	def test_create_get_pool(self):	
		self.target.process(["add","item","1"])
		self.target.process(["add","item2","2"])

		self.assertEquals(self.target.process(["show","item"]),"1")
		self.assertEquals(self.target.process(["show","item2"]),"2")

	def test_add_amounts(self):	
		self.target.process(["add","item","1"])
		self.assertEquals(self.target.process(["show","item"]),"1")
				
		self.target.process(["add","item","2"])
		self.assertEquals(self.target.process(["show","item"]),"3")
		
	def test_subtract(self):
		self.target.process(["add","item","4"])
		self.assertEquals(self.target.process(["show","item"]),"4")

		self.target.process(["subtract","item","1"])
		self.assertEquals(self.target.process(["show","item"]),"3")
		
		self.target.process(["subtract","item","2"])
		self.assertEquals(self.target.process(["show","item"]),"1")
		
	def test_subtract_untill_removal(self):
		self.target.process(["add","item","4"])
		self.target.process(["add","item2","4"])

		self.assertEquals(self.target.process(["show","item"]),"4")
		self.assertEquals(self.target.process(["show","item2"]),"4")

		self.target.process(["subtract","item","4"])
		self.assertEquals(self.target.process(["show","item"]),"**item** not found")
		
		self.target.process(["subtract","item2","5"])
		self.assertEquals(self.target.process(["show","item2"]),"**item** not found")
		
	def test_remove(self):
		self.target.process(["add","item","4"])
		self.assertEquals(self.target.process(["show","item"]),"4")
		
		self.target.process(["remove","item"])
		self.assertEquals(self.target.process(["show","item"]),"**item** not found")
		
	def test_show_all(self):
		self.assertEquals(self.target.process(["show"]),"No Combatants Entered")
	
		self.target.process(["add","item","1"])
		self.target.process(["add","item2","2"])
		
		self.assertEquals(self.target.process(["show"]),"**item**:1\n**item2**:2")

	def test_end(self):
		self.target.process(["add","item","1"])
		self.target.process(["add","item2","2"])
		self.assertEquals(self.target.process(["show"]),"**item**:1\n**item2**:2")

		self.target.process(["end"])

		self.assertEquals(self.target.process(["show"]),"No Combatants Entered")
		

	
if __name__ == "__main__":
	unittest.main()