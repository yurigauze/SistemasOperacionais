import os
import curses
import pycfg
from pyarch import load_binary_into_memory
from pyarch import cpu_t
from pyarch import terminal_t

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_msg = ""
		self.terminal.console_print("this is the console, type the commands here\n")
		self.terminal.console_print("digite 'fechar' para encerrar e 'carregar processo' para carregar um processo\n")
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
			self.console_msg  += chr(key)
			self.terminal.console_print("\r" + self.console_msg)

		elif key == curses.KEY_BACKSPACE:
			self.console_msg = self.console_msg[:-1]
			self.terminal.console_print("\r" + self.console_msg)


		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.execute_command(self.console_msg)
			self.console_msg  = ""




	def handle_interrupt (self, interrupt):
		if interrupt == 2:
			self.syscall(interrupt)
			self.interrupt_keyboard()
		else:
			self.syscall(interrupt)


	def execute_command(self, command):
		if command == "fechar":
			os.system('clear')
			exit()

		elif command == "carregar processo":
			self.printk("Processo Carregado") 

		elif command == "":
			return
		else:
			self.printk("comando desconhecido: %s" % command)

	def syscall (self,interrupt):
		if interrupt == 2:
			self.terminal.app_print("\nUma interrupcao do teclado foi recebida")
		elif interrupt == 3:
			self.terminal.app_print("\nUma interrupcao do time foi recebida")
		else:
			self.terminal.app_print("\nNao se sabe de onde veio a interrupcao")



class Process:
	def __init__(self, pid, regs, registerPc,  resources, text, state='pronto'):
		self.pid = pid #identificador do processo
		self.registerPc = registerPc #Program Counter
		self.regs[8] =  regs #registradores
		self.state = state #string do estado do processo
		self.resources = resources #lista de recursos associados como arquivos e dispositivos de entrada e saida
		self.text = text # codigo do processo

	def setState(self, state):
		self.state = state	

	def setRegs(self, value):
		self.regs = value

	def setRegPC(self, value):
		self.reg_pc = value
