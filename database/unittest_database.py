##
# @file   unittest_database.py
# @author Yibo Lin
# @date   Mar 2020
#

import pdb
import os
import sys
import unittest

if len(sys.argv) < 2:
    print("usage: python script.py [project_dir] test_dir")
    project_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
elif len(sys.argv) < 3:
    print("usage: python script.py [project_dir] test_dir")
    project_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    test_dir = sys.argv[1]
else:
    project_dir = sys.argv[1]
    test_dir = sys.argv[2]
print("use project_dir = %s" % (project_dir))

sys.path.append(project_dir)
import openparf.openparf as of
sys.path.pop()


class DatabaseTest(unittest.TestCase):
    def testSample1(self):
        db = of.database.Database(0)
        db.readBookshelf(test_dir + "/sample1/design.aux")
        design = db.design()

        # test model
        self.assertEqual(design.numModels(), 14)
        model_id = design.modelId("Bookshelf.TOP")
        model = design.model(model_id)
        if model.modelType() == of.ModelType.kModule:
            netlist = model.netlist()
            self.assertTrue(netlist)
            self.assertEqual(netlist.numInsts(), 12)
            self.assertEqual(netlist.numNets(), 5)
            for pin in netlist.pins():
                inst = netlist.inst(pin.instId())
                net = netlist.net(pin.netId())
                self.assertTrue(pin.id() in inst.pinIds())
                self.assertTrue(pin.id() in net.pinIds())
                self.assertEqual(inst.id(), netlist.inst(inst.id()).id())
                self.assertEqual(net.id(), netlist.net(net.id()).id())

        # test design
        top_module_inst_id = design.topModuleInstId()
        self.assertTrue(top_module_inst_id < design.numModuleInsts())
        top_module_inst = design.topModuleInst()
        self.assertTrue(top_module_inst)
        netlist = top_module_inst.netlist()
        for pin_id in netlist.pinIds():
            pin = netlist.pin(pin_id)
            inst = netlist.inst(pin.instId())
            net = netlist.net(pin.netId())
            self.assertTrue(pin.id() in inst.pinIds())
            self.assertTrue(pin.id() in net.pinIds())
            self.assertTrue(inst.id() in netlist.instIds())
            self.assertTrue(net.id() in netlist.netIds())

        layout = db.layout()

        # test layout
        site_map = layout.siteMap()
        self.assertTrue(site_map.width(), 150)
        self.assertTrue(site_map.height(), 300)
        for site in site_map:
            if layout.siteType(site).name() =="PLB":
                self.assertEqual(site.bbox().width(), 1)
                self.assertEqual(site.bbox().height(), 1)
            elif layout.siteType(site).name() == "DSP1":
                self.assertEqual(site.bbox().width(), 1)          
                self.assertEqual(site.bbox().height(), 3)
            elif layout.siteType(site).name() == "RAMA":
                self.assertEqual(site.bbox().width(), 1)
                self.assertEqual(site.bbox().height(), 3)
            elif layout.siteType(site).name() == "RAMB":
                self.assertEqual(site.bbox().width(), 1)
                self.assertEqual(site.bbox().height(), 5)
            elif layout.siteType(site).name() == "IOA":
                self.assertEqual(site.bbox().width(), 1)
                self.assertEqual(site.bbox().height(), 1)  
            elif layout.siteType(site).name() == "IOB":
                self.assertEqual(site.bbox().width(), 1)
                self.assertEqual(site.bbox().height(), 1)
            elif layout.siteType(site).name() == "IPPIN":
                self.assertEqual(site.bbox().width(), 1)
                self.assertEqual(site.bbox().height(),1
            elif layout.siteType(site).name() == "GCLK":
                self.assertEqual(site.bbox().width(), 1)
                self.assertEqual(site.bbox().height(), 1)              

        site_type_map = layout.siteTypeMap()
        resource_map = layout.resourceMap()
        self.assertEqual(
            site_type_map.siteType("PLB").resourceCapacity(
                resource_map.resourceId("LUT")), 8)
        self.assertEqual(
            site_type_map.siteType("PLB").resourceCapacity(
                resource_map.resourceId("FF")), 16)
        self.assertEqual(
            site_type_map.siteType("PLB").resourceCapacity(
                resource_map.resourceId("CARRY4")), 2)
        self.assertEqual(
            site_type_map.siteType("PLB").resourceCapacity(
                resource_map.resourceId("DRAM")), 2)             
        self.assertEqual(
            site_type_map.siteType("DSP1").resourceCapacity(
                resource_map.resourceId("DSP1")), 1)
        self.assertEqual(
            site_type_map.siteType("RAMA").resourceCapacity(
                resource_map.resourceId("RAMA")), 1)   
        self.assertEqual(
            site_type_map.siteType("RAMB").resourceCapacity(
                resource_map.resourceId("RAMB")), 1)   
        self.assertEqual(
            site_type_map.siteType("GCLK").resourceCapacity(
                resource_map.resourceId("GCLK")), 28)
                
        self.assertEqual(
            site_type_map.siteType("IOA").resourceCapacity(
                resource_map.resourceId("IOA")), 2)   
        self.assertEqual(
            site_type_map.siteType("IOB").resourceCapacity(
                resource_map.resourceId("IOB")), 2)      
        self.assertEqual(
            site_type_map.siteType("IPPIN").resourceCapacity(
                resource_map.resourceId("IPPIN")), 256)

        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("LUT1")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("LUT2")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("LUT3")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("LUT4")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("LUT5")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("LUT6")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("LUT6X")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("F7MUX")))
        self.assertTrue(
            resource_map.resourceId("LUT") in resource_map.modelResourceIds(
                design.modelId("F8MUX")))
        self.assertTrue(
            resource_map.resourceId("FF") in resource_map.modelResourceIds(
                design.modelId("SEQ")))
        self.assertTrue(
            resource_map.resourceId("CARRY4") in resource_map.modelResourceIds(
                design.modelId("CARRY4")))
        self.assertTrue(
            resource_map.resourceId("DSP1") in resource_map.modelResourceIds(
                design.modelId("DSP1")))
        self.assertTrue(
            resource_map.resourceId("DRAM") in resource_map.modelResourceIds(
                design.modelId("DRAM")))
        self.assertTrue(
            resource_map.resourceId("RAMA") in resource_map.modelResourceIds(
                design.modelId("RAMA")))
        self.assertTrue(
            resource_map.resourceId("RAMB") in resource_map.modelResourceIds(
                design.modelId("RAMB")))
	self.assertTrue(
            resource_map.resourceId("IOA") in resource_map.modelResourceIds(
                design.modelId("IOA")))
        self.assertTrue(
            resource_map.resourceId("IOB") in resource_map.modelResourceIds(
                design.modelId("IOB")))
        self.assertTrue(
            resource_map.resourceId("GCLK") in resource_map.modelResourceIds(
                design.modelId("GCLK")))
        self.assertTrue(
            resource_map.resourceId("IPPIN") in resource_map.modelResourceIds(
                design.modelId("IPPIN")))  
                      
        clock_region_map = layout.clockRegionMap()
        self.assertEqual(clock_region_map.width(), 5)
        self.assertEqual(clock_region_map.height(), 5)
        clock_region_x0y0 = clock_region_map.at(0, 0)
        self.assertEqual(clock_region_x0y0.bbox().xl(), 0)
        self.assertEqual(clock_region_x0y0.bbox().yl(), 0)
        self.assertEqual(clock_region_x0y0.bbox().xh(), 25)
        self.assertEqual(clock_region_x0y0.bbox().yh(), 59)
        clock_region_x0y1 = clock_region_map.at(0, 1)
        self.assertEqual(clock_region_x0y1.bbox().xl(), 0)
        self.assertEqual(clock_region_x0y1.bbox().yl(), 60)
        self.assertEqual(clock_region_x0y1.bbox().xh(), 25)
        self.assertEqual(clock_region_x0y1.bbox().yh(), 119)
        clock_region_x0y2 = clock_region_map.at(0, 2)
        self.assertEqual(clock_region_x0y2.bbox().xl(), 0)
        self.assertEqual(clock_region_x0y2.bbox().yl(), 120)
        self.assertEqual(clock_region_x0y2.bbox().xh(), 25)
        self.assertEqual(clock_region_x0y2.bbox().yh(), 179)
        clock_region_x0y3 = clock_region_map.at(0, 3)
        self.assertEqual(clock_region_x0y3.bbox().xl(), 0)
        self.assertEqual(clock_region_x0y3.bbox().yl(), 180)
        self.assertEqual(clock_region_x0y3.bbox().xh(), 25)
        self.assertEqual(clock_region_x0y3.bbox().yh(), 239)
        clock_region_x0y4 = clock_region_map.at(0, 4)
        self.assertEqual(clock_region_x0y3.bbox().xl(), 0)
        self.assertEqual(clock_region_x0y3.bbox().yl(), 240)
        self.assertEqual(clock_region_x0y3.bbox().xh(), 25)
        self.assertEqual(clock_region_x0y3.bbox().yh(), 299)        
        clock_region_x1y4 = clock_region_map.at(1, 4)
        self.assertEqual(clock_region_x1y3.bbox().xl(), 26)
        self.assertEqual(clock_region_x1y3.bbox().yl(), 240)
        self.assertEqual(clock_region_x1y3.bbox().xh(), 53)
        self.assertEqual(clock_region_x1y3.bbox().yh(), 299)
        clock_region_x2y0 = clock_region_map.at(2, 0)
        self.assertEqual(clock_region_x2y0.bbox().xl(), 54)
        self.assertEqual(clock_region_x2y0.bbox().yl(), 0)
        self.assertEqual(clock_region_x2y0.bbox().xh(), 85)
        self.assertEqual(clock_region_x2y0.bbox().yh(), 59)
        clock_region_x2y4 = clock_region_map(2, 4)
        self.assertEqual(clock_region_x2y7.bbox().xl(), 54)
        self.assertEqual(clock_region_x2y7.bbox().yl(), 240)
        self.assertEqual(clock_region_x2y7.bbox().xh(), 85)
        self.assertEqual(clock_region_x2y7.bbox().yh(), 299)
        clock_region_x3y0 = clock_region_map.at(3, 0)
        self.assertEqual(clock_region_x3y0.bbox().xl(), 86)
        self.assertEqual(clock_region_x3y0.bbox().yl(), 0)
        self.assertEqual(clock_region_x3y0.bbox().xh(), 113)
        self.assertEqual(clock_region_x3y0.bbox().yh(), 59)
        clock_region_x3y4 = clock_region_map(3, 4)
        self.assertEqual(clock_region_x3y7.bbox().xl(), 86)
        self.assertEqual(clock_region_x3y7.bbox().yl(), 240)
        self.assertEqual(clock_region_x3y7.bbox().xh(), 113)
        self.assertEqual(clock_region_x3y7.bbox().yh(), 299)
        clock_region_x4y0 = clock_region_map.at(4, 0)
        self.assertEqual(clock_region_x4y0.bbox().xl(), 114)
        self.assertEqual(clock_region_x4y0.bbox().yl(), 0)
        self.assertEqual(clock_region_x4y0.bbox().xh(), 149)
        self.assertEqual(clock_region_x4y0.bbox().yh(), 59)
        clock_region_x4y4 = clock_region_map(4, 4)
        self.assertEqual(clock_region_x4y7.bbox().xl(), 114)
        self.assertEqual(clock_region_x4y7.bbox().yl(), 240)
        self.assertEqual(clock_region_x4y7.bbox().xh(), 149)
        self.assertEqual(clock_region_x4y7.bbox().yh(), 299)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        pass
    elif len(sys.argv) < 3:
        sys.argv.pop()
    else:
        sys.argv.pop()
        sys.argv.pop()
    unittest.main()
