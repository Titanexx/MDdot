import argparse
from logger import LEVELS, init_logger, logger
from project import Project
import time

__version__ = 1.0
# Font ASCII : Georgia11
__banner__ = """

`7MMM.     ,MMF'`7MM\"""Yb.        `7MM           mm  
  MMMb    dPMM    MM    `Yb.        MM           MM   
  M YM   ,M MM    MM     `Mb   ,M""bMM  ,pW"Wq.mmMMmm 
  M  Mb  M' MM    MM      MM ,AP    MM 6W'   `Wb MM   
  M  YM.P'  MM    MM     ,MP 8MI    MM 8M     M8 MM   
  M  `YM'   MM    MM    ,dP' `Mb    MM YA.   ,A9 MM   
.JML. `'  .JMML..JMMmmmdP'    `Wbmd"MML.`Ybmd9'  `Mbmo

"""

def init_args():

	max_verbose_level = len(LEVELS)

	parser = argparse.ArgumentParser(description='%sCreate a docx file from a markdown file with a template file.' % __banner__ ,formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-o', '--output', help='Output filename', default='mddot_file_%s.docx' % int(time.time()))
	parser.add_argument('-V', '--version', action='version', version="MDdot Mk.%s" % (__version__), help='Print version',)
	parser.add_argument('-v', '--verbose', help='Change log output level from 0 to %s : %s' % (max_verbose_level,LEVELS), default='0', type=int)
	requiredNamed = parser.add_argument_group('Required arguments')
	requiredNamed.add_argument('-m', '--md', help='Input markdown filename', required=True)
	requiredNamed.add_argument('-d', '--docx', help='Input docx template filename', required=True)
	
	args = parser.parse_args()

	if args.verbose < 0:
		args.verbose = 0
	elif args.verbose >= max_verbose_level:
		args.verbose = max_verbose_level -1

	init_logger(args.verbose)

	return args

if __name__ == '__main__':
	args  = init_args()

	Project(args.md,args.docx,args.output)