from neuron import h

from cells.core.basic_cell import BasicCell


class PointProcessCell(BasicCell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        BasicCell.__init__(self, name)
        self.pprocs = {}
        self.pprocs_num = 0

    def filter_pprocs(self, pp_type: str, sec_names, as_list=False):
        """
        All sec_names must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is sec_name and [0] is index of the point process of the specific type.

        :param pp_type:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for self.pprocs keys which contains each point_process_names.
            None or 'all' will add to all point processes.
        :param as_list:
        :return:
        """
        return self._filter_obj_dict("pprocs", mech_type=pp_type, names=sec_names, as_list=as_list)

    def add_pprocs(self, name, sec_names, loc, **kwargs):
        """
        :param name:
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will add point process to all secs.
        :param loc:
        :param kwargs:
        :return:
            A list of added Point Processes
        """
        result = []
        if not hasattr(h, name):
            raise LookupError("There is no Point Process of name %s. "
                              "Maybe you forgot to compile or copy mod files?" % name)
        pp = getattr(h, name)
        sec_names = self._filter_obj_dict("secs", names=sec_names)

        for sec_name, sec in sec_names.items():
            pp_instance = pp(sec(loc))
            result.append(pp_instance)

            #for key, value in kwargs.items():
            #    if not hasattr(pp_instance, key):
            #        raise LookupError("Point Process of type %s has no attribute of type %s. "
            #                          "Check if MOD file contains %s as a RANGE variable" % (name, key, key))
            #    setattr(pp_instance, key, value)

            self.pprocs["%s_%s[%s]" % (name, sec_name, self.pprocs_num)] = pp_instance
            self.pprocs_num += 1

        return result
