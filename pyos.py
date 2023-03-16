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
		print("AQUI")

	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")
		print("AQUI")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False
		print("AQUI")

	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		if key == curses.KEY_BACKSPACE:
		    #Apaga o ultimo digito da string de console
        		self.console_str = self.console_str[:-1]
		    #Atualizar o console
		    	self.terminal.console_print("\rDigite os comandos aqui: " + self.console_str + " ")
		    	self.terminal.refresh()
		elif (key == curses.KEY_ENTER):
		    #Executar o comando digitado pelo usuario
		    self.terminal.console_print("\n")
		    self.execute_command()
		    self.console_str = ""
		elif ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
        	#Adicionar o caractere digitado a string de console
		    self.console_str += chr(key)
		    #Atualizar o console
		    self.terminal.console_print(chr(key))
		    self.terminal.refresh()

	def handle_interrupt (self, interrupt):
		# Verifica se a interrucaoca e do teclado (IRQ1)
		print("sera que foi?")
		if interrupt.type == 2:
			self.interrupt_keyboard()
		else:
			return

	def syscall (self):
		#self.terminal.app_print(msg)
		return
