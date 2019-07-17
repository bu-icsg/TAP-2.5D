from system import System_25D

class PassiveInterposer(System_25D):
	"""docstring for Passive"""
	def __init__(self):
		super().__init__()

	def gen_flp(self, filename):
		# material properties
		UnderFill = "\t2.32E+06\t0.625\n"
		Copper = "\t3494400\t0.0025\n"
		Silicon = "\t1.75E+06\t0.01\n"
		resistivity_Cu = 0.0025
		resistivity_UF = 0.625
		resistivity_Si = 0.01
		specHeat_Cu = 3494400
		specHeat_UF = 2320000
		specHeat_Si = 1750000
		C4_diameter 	= 0.000250		#250um
		C4_edge 		= 0.000600 		#600um
		TSV_diameter 	= 0.000010		#10um  
		TSV_edge		= 0.000050		#50um  
		ubump_diameter 	= 0.000025		#25um
		ubump_edge 		= 0.000050		#50um  		
		Aratio_C4 = (C4_edge/C4_diameter)*(C4_edge/C4_diameter)-1			# ratio of white area and C4 area
		Aratio_TSV= (TSV_edge/TSV_diameter)*(TSV_edge/TSV_diameter)-1
		Aratio_ubump=(ubump_edge/ubump_diameter)*(ubump_edge/ubump_diameter)-1
		resistivity_C4=(1+Aratio_C4)*resistivity_Cu*resistivity_UF/(resistivity_UF+Aratio_C4*resistivity_Cu)
		resistivity_TSV=(1+Aratio_TSV)*resistivity_Cu*resistivity_Si/(resistivity_Si+Aratio_TSV*resistivity_Cu)
		resistivity_ubump=(1+Aratio_ubump)*resistivity_Cu*resistivity_UF/(resistivity_UF+Aratio_ubump*resistivity_Cu)
		specHeat_C4=(specHeat_Cu+Aratio_C4*specHeat_UF)/(1+Aratio_C4)
		specHeat_TSV=(specHeat_Cu+Aratio_TSV*specHeat_Si)/(1+Aratio_TSV)
		specHeat_ubump=(specHeat_Cu+Aratio_ubump*specHeat_UF)/(1+Aratio_ubump)
		mat_C4 = "\t"+str(specHeat_C4)+"\t"+str(resistivity_C4)+"\n"
		mat_TSV = "\t"+str(specHeat_TSV)+"\t"+str(resistivity_TSV)+"\n"
		mat_ubump = "\t"+str(specHeat_ubump)+"\t"+str(resistivity_ubump)+"\n"

		with open(self.path + filename+ 'L0_Substrate.flp','w') as L0_Substrate:
			L0_Substrate.write("# Floorplan for Substrate Layer with size "+str(self.intp_size/1000)+"x"+str(self.intp_size/1000)+" m\n")
			L0_Substrate.write("# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat>]\\t[<resistivity>]\n")
			L0_Substrate.write("# all dimensions are in meters\n")
			L0_Substrate.write("# comment lines begin with a '#' \n")
			L0_Substrate.write("# comments and empty lines are ignored\n\n")
			L0_Substrate.write("Substrate\t"+str(self.intp_size/1000)+"\t"+str(self.intp_size/1000)+"\t0.0\t0.0\n")

		os.system("perl util/tofig.pl -f 20 "+self.path+filename+"L0_Substrate.flp | fig2dev -L ps | ps2pdf - "+self.path+filename+"L0_Substrate.pdf")


	# print floorplans into pdf files
	# print "plotting floorplans......................."
	# os.system("perl tofig.pl -f 20 "+path+filename+"L1_C4Layer.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L1_C4Layer.pdf")
	# os.system("perl tofig.pl -f 20 "+path+filename+"L2_Interposer.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L2_Interposer.pdf")
	# os.system("perl tofig.pl -f 4 "+path+filename+"L3_UbumpLayer.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L3_UbumpLayer.pdf")
	# os.system("perl tofig.pl -f 4 "+path+filename+"L3.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L3.pdf")
	# os.system("perl tofig.pl -f 4 "+path+filename+"L4_Cores.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L4_Cores.pdf")
	# os.system("perl tofig.pl -f 4 "+path+filename+"L4.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L4.pdf")
	# os.system("perl tofig.pl -f 20 "+path+filename+"L5_TIM.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L5_TIM.pdf")
