from ..src.controllers.schedule import schedule_generation
import unittest


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_schedule_1(self):
        try:
            interest = 12
            term = 24
            principal_amount = 1000000
            answer = {1: (-37073.47, -10000.00),
                      2: (-37444.21, -9629.27),
                      3: (-37818.65, -9254.82),
                      4: (-38196.84, -8876.64),
                      5: (-38578.80, -8494.67),
                      6: (-38964.59, -8108.88),
                      7: (-39354.24, -7719.23),
                      8: (-39747.78, -7325.69),
                      9: (-40145.26, -6928.21),
                      10: (-40546.71, -6526.76),
                      11: (-40952.18, -6121.29),
                      12: (-41361.70, -5711.77),
                      13: (-41775.32, -5298.16),
                      14: (-42193.07, -4880.40),
                      15: (-42615.00, -4458.47),
                      16: (-43041.15, -4032.32),
                      17: (-43471.56, -3601.91),
                      18: (-43906.28, -3167.19),
                      19: (-44345.34, -2728.13),
                      20: (-44788.79, -2284.68),
                      21: (-45236.68, -1836.79),
                      22: (-45689.05, -1384.42),
                      23: (-46145.94, -927.53),
                      24: (-46607.40, -466.07)}
            schedule = await schedule_generation(interest, term, principal_amount)
            for key in schedule:
                self.assertTrue(schedule[key] == answer[key])
        except Exception:
            self.fail("Caught exception")

    async def test_schedule_2(self):
        try:
            interest = 90
            term = 8
            principal_amount = 10000
            answer = {1: (-957.27, -750.00),
                      2: (-1029.07, -678.20),
                      3: (-1106.25, -601.02),
                      4: (-1189.21, -518.06),
                      5: (-1278.40, -428.87),
                      6: (-1374.29, -332.99),
                      7: (-1477.36, -229.91),
                      8: (-1588.16, -119.11)}
            schedule = await schedule_generation(interest, term, principal_amount)
            for key in schedule:
                self.assertTrue(schedule[key] == answer[key])
        except Exception:
            self.fail("Caught exception")

    async def test_schedule_3(self):
        try:
            interest = 22
            term = 36
            principal_amount = 500000
            answer = {1: (-9928.56, -9166.67),
                      2: (-10110.58, -8984.64),
                      3: (-10295.94, -8799.28),
                      4: (-10484.70, -8610.52),
                      5: (-10676.92, -8418.30),
                      6: (-10872.67, -8222.56),
                      7: (-11072.00, -8023.23),
                      8: (-11274.99, -7820.24),
                      9: (-11481.69, -7613.53),
                      10: (-11692.19, -7403.04),
                      11: (-11906.55, -7188.68),
                      12: (-12124.83, -6970.39),
                      13: (-12347.12, -6748.10),
                      14: (-12573.49, -6521.74),
                      15: (-12804.00, -6291.23),
                      16: (-13038.74, -6056.49),
                      17: (-13277.78, -5817.44),
                      18: (-13521.21, -5574.02),
                      19: (-13769.10, -5326.13),
                      20: (-14021.53, -5073.69),
                      21: (-14278.59, -4816.63),
                      22: (-14540.37, -4554.86),
                      23: (-14806.94, -4288.28),
                      24: (-15078.40, -4016.82),
                      25: (-15354.84, -3740.39),
                      26: (-15636.35, -3458.88),
                      27: (-15923.01, -3172.21),
                      28: (-16214.93, -2880.29),
                      29: (-16512.21, -2583.02),
                      30: (-16814.93, -2280.30),
                      31: (-17123.21, -1972.02),
                      32: (-17437.13, -1658.10),
                      33: (-17756.81, -1338.42),
                      34: (-18082.35, -1012.87),
                      35: (-18413.86, -681.36),
                      36: (-18751.45, -343.78)}
            schedule = await schedule_generation(interest, term, principal_amount)
            for key in schedule:
                self.assertTrue(schedule[key] == answer[key])
        except Exception:
            self.fail("Caught exception")


if __name__ == '__main__':
    unittest.main()
