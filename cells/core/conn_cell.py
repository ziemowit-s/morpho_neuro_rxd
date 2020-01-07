from cells.core.point_process_cell import PointProcessCell
from cells.core.utils import get_conn


class ConnCell(PointProcessCell):
    def __init__(self, name):
        PointProcessCell.__init__(self, name)
        self.conns = {}
        self.conn_num = 0

    def filter_conns(self, pp_type, sec_names, as_list=False):
        """
        :param pp_type:
            single string defining name of target point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will return all conns.
        :param as_list:
        :return:
        """
        return self._filter_obj_dict("conns", mech_type=pp_type, names=sec_names, as_list=as_list)

    def add_conn(self, source, weight, pp_type=None, sec_names=None, delay=0):
        """
        :param source:
        :param weight:
        :param pp_type:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for self.pprocs keys which contains each point_process_names.
            None or 'all' will add to all point processes.
        :param delay:
        return:
            A list of added NetConns.
        """
        results = []
        conn_names = self.filter_pprocs(pp_type=pp_type, sec_names=sec_names)

        for name, syn in conn_names.items():
            conn = get_conn(source=source, target=syn, delay=delay, weight=weight)
            self.conns["%s_%s[%s]" % (pp_type, name, self.conn_num)] = conn
            self.conn_num += 1
            results.append(conn)

        return results
