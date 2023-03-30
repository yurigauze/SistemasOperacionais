import os
import curses
import pycfg
from pyarch import load_binary_into_memory
from pyarch import cpu_t

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_str = ""
		self.terminal.console_print("this is the console, type the commands here\n")
		self.keyboard_buffer = ""

	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False

	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
			self.console_str  += chr(key)
			self.terminal.console_print("\r" + self.console_str)

		elif key == curses.KEY_BACKSPACE:
			self.console_str = self.console_str[:-1]
			self.terminal.clear()
			self.terminal.console_print(self.console_str)
			return

		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.execute_command(self.console_str)
			self.console_str  = ""




	def handle_interrupt (self, interrupt):
		if interrupt == 2:
			self.printk("interrupcao recebida: %d" % interrupt)
			self.interrupt_keyboard()
		else:
			self.printk("interrupcao recebida: %d" % interrupt)


	def execute_command(self, command):
		if command == "fechar":
			os.system('clear')
			os.kill(os.getpid(), 2)
			os.system('clear')
		elif command == "carregar":
			self.printk("Carregado")
		else:
			self.printk("comando desconhecido: %s" % command)

	def syscall (self):
		#self.terminal.app_print(msg)
		return
