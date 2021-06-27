import persist
import personal_library
import cProfile
import pstats
from pstats import SortKey

cProfile.run('personal_library.create(\'books\')', 'cStats')
p = pstats.Stats('qStats')
p.strip_dirs().sort_stats(SortKey.TIME).print_stats()

cProfile.run('personal_library.search(\'books\', \'network\')', 'qStats')
p = pstats.Stats('cStats')
p.strip_dirs().sort_stats(SortKey.TIME).print_stats()
