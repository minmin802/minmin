/**
 * @file   database.cpp
 * @author Yibo Lin
 * @date   Mar 2020
 */

#include "database/database.h"
#include <fstream>
#include <gtest/gtest.h>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

extern std::string test_dir;

OPENPARF_BEGIN_NAMESPACE

namespace unitest {

/// GTest class for fft module testing
class DatabaseTest : public ::testing::Test {
public:
  void testSample1() {
    openparf::database::Database db(0);
    db.readBookshelf(test_dir + "/" + "../../benchmarks/sample1/design.aux");

    std::cout << db.design() << std::endl;
    // std::cout << db << std::endl;

    auto const &design = db.design();
    auto const &layout = db.layout();
    auto const &site_map = layout.siteMap();
    for (auto const &site : site_map) {
      ASSERT_EQ(
          &site,
          &site_map.at(site.siteMapId().x(), site.siteMapId().y()).value());
      if (layout.siteType(site).name() == "PLB") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 1);
      } else if (layout.siteType(site).name() == "DSP1") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 3);      
      } else if (layout.siteType(site).name() == "RAMA") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 3);
      } else if (layout.siteType(site).name() == "RAMB") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 5);
      } else if (layout.siteType(site).name() == "GCLK") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 1);
      } else if (layout.siteType(site).name() == "IOA") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 1);
      } else if (layout.siteType(site).name() == "IOB") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 1);
      } else if (layout.siteType(site).name() == "IPPIN") {
        ASSERT_EQ(site.bbox().width(), 1);
        ASSERT_EQ(site.bbox().height(), 1);
      } 
      
    auto const &site_type_map = layout.siteTypeMap();
    auto const &resource_map = layout.resourceMap();
    ASSERT_EQ(site_type_map.siteType("PLB")->resourceCapacity(
                  resource_map.resourceId("LUT")),
              8);
    ASSERT_EQ(site_type_map.siteType("PLB")->resourceCapacity(
                  resource_map.resourceId("FF")),
              16);
    ASSERT_EQ(site_type_map.siteType("PLB")->resourceCapacity(
                  resource_map.resourceId("CARRY4")),
              2);
    ASSERT_EQ(site_type_map.siteType("PLB")->resourceCapacity(
                  resource_map.resourceId("DRAM")),
              2);              
    ASSERT_EQ(site_type_map.siteType("DSP1")->resourceCapacity(
                  resource_map.resourceId("DSP1")),
              1);
    ASSERT_EQ(site_type_map.siteType("RAMA")->resourceCapacity(
                  resource_map.resourceId("RAMA")),
              1);
    ASSERT_EQ(site_type_map.siteType("RAMB")->resourceCapacity(
                  resource_map.resourceId("RAMB")),
              1);
    ASSERT_EQ(site_type_map.siteType("GCLK")->resourceCapacity(
                  resource_map.resourceId("GCLK")),
              28);
    ASSERT_EQ(site_type_map.siteType("IOA")->resourceCapacity(
                  resource_map.resourceId("IOA")),
              2);
    ASSERT_EQ(site_type_map.siteType("IOB")->resourceCapacity(
                  resource_map.resourceId("IOB")),
              2);                            
    ASSERT_EQ(site_type_map.siteType("IPPIN")->resourceCapacity(
                  resource_map.resourceId("IPPIN")),
              256);

    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("LUT1"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("LUT2"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("LUT3"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("LUT4"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("LUT5"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("LUT6"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("LUT6X"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("F7MUX"))[0]);
    ASSERT_EQ(resource_map.resourceId("LUT"),
              resource_map.modelResourceIds(design.modelId("F8MUX"))[0]);
    ASSERT_EQ(resource_map.resourceId("FF"),
                  resource_map.modelResourceIds(design.modelId("SEQ"))[0]);
    ASSERT_EQ(resource_map.resourceId("CARRY4"),
              resource_map.modelResourceIds(design.modelId("CARRY4"))[0]);
    ASSERT_EQ(resource_map.resourceId("DSP1"),
              resource_map.modelResourceIds(design.modelId("DSP1"))[0]);
    ASSERT_EQ(resource_map.resourceId("RAMA"),
              resource_map.modelResourceIds(design.modelId("RAMA"))[0]);
    ASSERT_EQ(resource_map.resourceId("RAMB"),
              resource_map.modelResourceIds(design.modelId("RAMB"))[0]);
    ASSERT_EQ(resource_map.resourceId("IOA"),
              resource_map.modelResourceIds(design.modelId("IOA"))[0]);
    ASSERT_EQ(resource_map.resourceId("IOB"),
              resource_map.modelResourceIds(design.modelId("IOB"))[0]);
    ASSERT_EQ(resource_map.resourceId("GCLK"),
              resource_map.modelResourceIds(design.modelId("GCLK"))[0]);
    ASSERT_EQ(resource_map.resourceId("IPPIN"),
              resource_map.modelResourceIds(design.modelId("IPPIN"))[0]);                                          
  }
};

TEST_F(DatabaseTest, Sample1) { testSample1(); }

} // namespace unitest

OPENPARF_END_NAMESPACE
