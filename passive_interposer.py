from system import System_25D
import os
import util.fill_space

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

		with open(self.path+filename +'L1_C4Layer.flp','w') as L1_C4Layer:
			L1_C4Layer.write("# Floorplan for C4 Layer \n")
			L1_C4Layer.write("# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat>]\\t[<resistivity>]\n")
			L1_C4Layer.write("# all dimensions are in meters\n")
			L1_C4Layer.write("# comment lines begin with a '#' \n")
			L1_C4Layer.write("# comments and empty lines are ignored\n\n")
			L1_C4Layer.write("C4Layer\t"+str(self.intp_size / 1000)+"\t"+str(self.intp_size / 1000)+"\t0.0\t0.0"+mat_C4)
		os.system("perl util/tofig.pl -f 20 "+self.path+filename+"L1_C4Layer.flp | fig2dev -L ps | ps2pdf - "+self.path+filename+"L1_C4Layer.pdf")

		with open(self.path+filename +'L2_Interposer.flp','w') as L2_Interposer:
			L2_Interposer.write("# Floorplan for Silicon Interposer Layer\n")
			L2_Interposer.write("# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat>]\\t[<resistivity>]\n")
			L2_Interposer.write("# all dimensions are in meters\n")
			L2_Interposer.write("# comment lines begin with a '#' \n")
			L2_Interposer.write("# comments and empty lines are ignored\n\n")
			L2_Interposer.write("Interposer\t"+str(self.intp_size / 1000)+"\t"+str(self.intp_size / 1000)+"\t0.0\t0.0"+mat_TSV)
		os.system("perl util/tofig.pl -f 20 "+self.path+filename+"L2_Interposer.flp | fig2dev -L ps | ps2pdf - "+self.path+filename+"L2_Interposer.pdf")

		with open(self.path+filename + 'sim.flp','w') as SIMP:
			with open(self.path + filename + 'L3.flp', 'w') as L3_UbumpLayer:
				with open(self.path + filename + 'L4.flp', 'w') as L4_ChipLayer:
					L3_UbumpLayer.write("# Floorplan for Microbump Layer \n")
					L3_UbumpLayer.write("# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat>]\\t[<resistivity>]\n")
					L3_UbumpLayer.write("# all dimensions are in meters\n")
					L3_UbumpLayer.write("# comment lines begin with a '#' \n")
					L3_UbumpLayer.write("# comments and empty lines are ignored\n\n")
					L4_ChipLayer.write("# Floorplan for Chip Layer\n")
					L4_ChipLayer.write("# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat>]\\t[<resistivity>]\n")
					L4_ChipLayer.write("# all dimensions are in meters\n")
					L4_ChipLayer.write("# comment lines begin with a '#' \n")
					L4_ChipLayer.write("# comments and empty lines are ignored\n\n")

					x_offset0, y_offset0 = 0, 0
					index_ubump = 0
					for i in range(0, self.chiplet_count):
						x_offset1 = x_offset0 + self.x[i] / 1000 - self.width[i] / 1000 * 0.5
						y_offset1 = y_offset0 + self.y[i] / 1000 - self.height[i] / 1000 * 0.5
						if self.ubump > 0:
							L3_UbumpLayer.write("Ubump_"+str(index_ubump)+"\t"+str(self.width[i] / 1000 - self.ubump / 1000)+"\t"+str(self.ubump / 1000)+"\t"+str(x_offset1)+"\t"+str(y_offset1)+mat_ubump)
							L3_UbumpLayer.write("Ubump_"+str(index_ubump+1)+"\t"+str(self.ubump / 1000)+"\t"+str(self.height[i] / 1000 - self.ubump / 1000)+"\t"+str(x_offset1)+"\t"+str(y_offset1+self.ubump / 1000)+mat_ubump)
							L3_UbumpLayer.write("Ubump_"+str(index_ubump+2)+"\t"+str(self.ubump / 1000)+"\t"+str(self.height[i] / 1000 - self.ubump / 1000)+"\t"+str(x_offset1+self.width[i] / 1000 - self.ubump / 1000)+"\t"+str(y_offset1)+mat_ubump)
							L3_UbumpLayer.write("Ubump_"+str(index_ubump+3)+"\t"+str(self.width[i] / 1000 - self.ubump / 1000)+"\t"+str(self.ubump / 1000)+"\t"+str(x_offset1+self.ubump / 1000)+"\t"+str(y_offset1+self.height[i] / 1000 - self.ubump / 1000)+mat_ubump)
							L4_ChipLayer.write("Ubump_"+str(index_ubump)+"\t"+str(self.width[i] / 1000 - self.ubump / 1000)+"\t"+str(self.ubump / 1000)+"\t"+str(x_offset1)+"\t"+str(y_offset1)+Silicon)
							L4_ChipLayer.write("Ubump_"+str(index_ubump+1)+"\t"+str(self.ubump / 1000)+"\t"+str(self.height[i] / 1000 - self.ubump / 1000)+"\t"+str(x_offset1)+"\t"+str(y_offset1+self.ubump / 1000)+Silicon)
							L4_ChipLayer.write("Ubump_"+str(index_ubump+2)+"\t"+str(self.ubump / 1000)+"\t"+str(self.height[i] / 1000 - self.ubump / 1000)+"\t"+str(x_offset1+self.width[i] / 1000 - self.ubump / 1000)+"\t"+str(y_offset1)+Silicon)
							L4_ChipLayer.write("Ubump_"+str(index_ubump+3)+"\t"+str(self.width[i] / 1000 - self.ubump / 1000)+"\t"+str(self.ubump / 1000)+"\t"+str(x_offset1+self.ubump / 1000)+"\t"+str(y_offset1+self.height[i] / 1000 - self.ubump / 1000)+Silicon)
						index_ubump += 4
						# not sure about the microbump density for the center region. Assume the same as the edge area so far. Need to be updated if the microbump pitch for center power/gnd clk is found
						L3_UbumpLayer.write("Chiplet_"+str(i)+"\t"+str(self.width[i] / 1000 - self.ubump / 1000 * 2)+"\t"+str(self.height[i] / 1000 - self.ubump / 1000 * 2)+"\t"+str(x_offset1 + self.ubump / 1000)+"\t"+str(y_offset1+self.ubump / 1000)+mat_ubump)
						L4_ChipLayer.write("Chiplet_"+str(i)+"\t"+str(self.width[i] / 1000 - self.ubump / 1000 * 2)+"\t"+str(self.height[i] / 1000 - self.ubump / 1000 * 2)+"\t"+str(x_offset1 + self.ubump / 1000)+"\t"+str(y_offset1+self.ubump / 1000)+Silicon)
						SIMP.write("Unit_"+str(i)+"\t"+str(self.width[i] / 1000)+"\t"+str(self.height[i] / 1000)+"\t"+str(x_offset1)+"\t"+str(y_offset1)+"\n")
		os.system("perl util/tofig.pl -f 20 "+self.path+filename+"L3.flp | fig2dev -L ps | ps2pdf - "+self.path+filename+"L3.pdf")
		os.system("perl util/tofig.pl -f 20 "+self.path+filename+"L4.flp | fig2dev -L ps | ps2pdf - "+self.path+filename+"L4.pdf")

		util.fill_space.fill_space(x_offset0,x_offset0+self.intp_size / 1000, y_offset0, y_offset0+self.intp_size / 1000, self.path+filename+'sim', self.path+filename+'L3', self.path+filename+'L3_UbumpLayer')
		util.fill_space.fill_space(x_offset0,x_offset0+self.intp_size / 1000, y_offset0, y_offset0+self.intp_size / 1000, self.path+filename+'sim', self.path+filename+'L4', self.path+filename+'L4_ChipLayer')
		os.system("perl util/tofig.pl -f 20 "+self.path+filename+"L3_UbumpLayer.flp | fig2dev -L ps | ps2pdf - "+self.path+filename+"L3_UbumpLayer.pdf")
		os.system("perl util/tofig.pl -f 20 "+self.path+filename+"L4_ChipLayer.flp | fig2dev -L ps | ps2pdf - "+self.path+filename+"L4_ChipLayer.pdf")





	# os.system("perl tofig.pl -f 20 "+path+filename+"L5_TIM.flp | fig2dev -L ps | ps2pdf - "+path+filename+"L5_TIM.pdf")
