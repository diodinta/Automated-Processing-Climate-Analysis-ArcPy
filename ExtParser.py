import ConfigParser
import re

class ExtParser(ConfigParser.SafeConfigParser):
     #implementing extended interpolation
     def __init__(self, *args, **kwargs):
         self.cur_depth = 0
         ConfigParser.SafeConfigParser.__init__(self, *args, **kwargs)


     def get(self, section, option, raw=False, vars=None):
         r_opt = ConfigParser.SafeConfigParser.get(self, section, option, raw=True, vars=vars)
         if raw:
             return r_opt

         ret = r_opt
         re_oldintp = r'%\((\w*)\)s'
         re_newintp = r'\$\{(\w*):(\w*)\}'

         m_new = re.findall(re_newintp, r_opt)
         if m_new:
             for f_section, f_option in m_new:
                 self.cur_depth = self.cur_depth + 1
                 if self.cur_depth < ConfigParser.MAX_INTERPOLATION_DEPTH:
                     sub = self.get(f_section, f_option, vars=vars)
                     ret = ret.replace('${{{0}:{1}}}'.format(f_section, f_option), sub)
                 else:
                     raise ConfigParser.InterpolationDepthError, (option, section, r_opt)



         m_old = re.findall(re_oldintp, r_opt)
         if m_old:
             for l_option in m_old:
                 self.cur_depth = self.cur_depth + 1
                 if self.cur_depth < ConfigParser.MAX_INTERPOLATION_DEPTH:
                     sub = self.get(section, l_option, vars=vars)
                     ret = ret.replace('%({0})s'.format(l_option), sub)
                 else:
                     raise ConfigParser.InterpolationDepthError, (option, section, r_opt)

         self.cur_depth = self.cur_depth - 1
         return ret
