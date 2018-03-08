#!/usr/bin/env python
'''
Created on Jan 14, 2011
Script to execute Anapsid.
Use signal 12 to terminate the script and obtain the results until that moment

@maintainer: Simon Castillo
@author: Maribel Acosta
@author: Gabriela Montoya

Last modification: June, 2013.
'''

import getopt
import sys, os, signal
import string
from multiprocessing import Process, Queue, active_children, Manager
from time import time
from Engine.Decomposer import decomposer
from Engine.Planner import Plan

from Engine.Planner.Plan import contactSource, contactProxy
import traceback


def runQuery(query_file, endpoint_file, buffer_size, simulated, endpointType, res):

    if simulated:
        contact = contactProxy
    else:
        contact = contactSource
    query = open(query_file).read()
    pos = string.rfind(query_file, "/")
    qu = query_file[pos + 1:]
    pos2 = string.rfind(qu, ".")
    if pos2 > -1:
        qu = qu[:pos2]
    global qname
    global t1
    global tn
    global c1
    global cn
    global dt
    global pt
    c1 = 0
    cn = 0
    t1 = -1
    tn = -1
    dt = -1
    global time1
    qname = qu
    time1 = time()
    new_query = decomposer.makePlan(query, endpoint_file)
    print(new_query)
    dt = time() - time1
    # if (p == "d") or (k == "y"):  # to show the decomposition or the plan
    #     print str(new_query)
    #     return
    # elif (k == "c"):  # to show the input for rdf3x
    #     print str(new_query.show2())
    #     return

    if (new_query == None):  # if the query could not be answered by the endpoints
        time2 = time() - time1
        t1 = time2
        tn = time2
        pt = time2
        printInfo()
        return
    plan = Plan.createPlan(new_query, adaptive=True, wc=True, buffersize=buffer_size, c=contact, endpointType=endpointType)

    pt = time() - time1
    # print 'creando procesos'
    p2 = Process(target=plan.execute, args=(res,))
    p2.start()
    p3 = Process(target=conclude, args=(res, False, t1, tn, c1, cn, time1, qname, dt, pt))
    p3.start()
    signal.signal(signal.SIGTERM, onSignal1)

    while True:
        if p2.is_alive() and not p3.is_alive():
            try:
                os.kill(p2.pid, 9)
            except Exception as ex:
                continue
            break
        elif not p2.is_alive() and not p3.is_alive():
            break


def conclude(res, printResults, _t1, _tn, _c1, _cn, _time1, _qname, _dt, _pt):
    signal.signal(signal.SIGTERM, onSignal2)
    global t1
    global tn
    global c1
    global cn
    global time1
    global qname
    global dt
    global pt
    t1 = _t1
    tn = _tn
    c1 = _c1
    cn = _cn
    dt = _dt
    time1 = _time1
    qname = _qname
    pt = _pt
    ri = res.get()
    if (printResults):
        if (ri == "EOF"):
            time2 = time() - time1
            t1 = time2
            tn = time2
            print "Empty set."
            printInfo()
            return

        while (ri != "EOF"):
            cn = cn + 1
            if cn == 1:
                time2 = time() - time1
                t1 = time2
                c1 = 1
            print ri
            ri = res.get(True)
        printInfo()
    else:
        if (ri == "EOF"):
            time2 = time() - time1
            t1 = time2
            tn = time2
            printInfo()
            return

        while (ri != "EOF"):
            cn = cn + 1
            if cn == 1:
                time2 = time() - time1
                t1 = time2
                c1 = 1
            # print ri
            ri = res.get(True)
        printInfo()


def printInfo():
    global tn
    if tn == -1:
        tn = time() - time1
    l = (qname + "\t" + str(dt) + "\t" + str(pt) + "\t" + str(t1) + "\t"
         + str(tn) + "\t" + str(c1) + "\t" + str(cn))
    print l


def onSignal1(s, stackframe):
    print ('entre en Signal1')
    cs = active_children()
    for c in cs:
        try:
            os.kill(c.pid, s)
        except OSError as ex:
            continue
    sys.exit(s)


def onSignal2(s, stackframe):
    print('entre en Signal2')
    printInfo()
    sys.exit(s)


def usage():
    usage_str = ("Usage: {program} -e <endpoints_file> -q <query_file>")
    print(usage_str.format(program=sys.argv[0])),


def  get_options(argv):
    try:
        opts, args = getopt.getopt(argv, "h:e:q:st")
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    endpointfile = None
    queryfile = None
    buffersize = 16384
    endpointType = False
    printResults = False
    simulated = False

    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt == "-e":
            endpointfile = arg
        elif opt == "-q":
            queryfile = arg
        elif opt == "-b":
            buffersize = int(arg)
        elif opt == "-s":
            simulated = True
        elif opt == '-t':
            endpointType = True

    if not endpointfile or not queryfile:
        usage()
        sys.exit(1)
    return (endpointfile, queryfile, buffersize, simulated, endpointType)


def main(argv):
    # manager = Manager()
    # res = manager.Queue()
    res = Queue()
    time1 = time()
    (endpoint, query, buffersize, simulated, endpointType) = get_options(argv[1:])
    try:
        runQuery(query, endpoint, buffersize, simulated, endpointType, res)
    except Exception as ex:
        print(traceback.format_exc())
        # print(ex)


if __name__ == '__main__':
    main(sys.argv)
