#!/usr/bin/env python

def main():
    import neutube
    import sys
    import json
    from libdvid import DVIDNodeService, ConnectionMethod
    import tempfile
    import numpy

    # parse commands
    # command: "<prog> <server> <uuid> <segmentationname> <body id> <synname>"
    dvidserver = sys.argv[1]
    uuid = sys.argv[2]
    skeletonname = sys.argv[3] + "_skeletons"
    todoname = sys.argv[3] + "_todo"
    bodyid = sys.argv[4]
    labelblk = sys.argv[3]
    synname = sys.argv[5]

    # PSD distance filter
    synfilter = 10
    annfilter = 10

    # retrieve skeleton
    ns = DVIDNodeService(dvidserver, uuid)
    f = tempfile.NamedTemporaryFile(delete=False)
    tempname = f.name
    f.write(ns.get(skeletonname, bodyid + "_swc"))
    f.close()

    # extract tips
    tree=neutube.ZSwcTree()
    tree.load(tempname)
    result = tree.computeAllTerminalDirection()

    # retrieve and load synapses
    syndata = ns.custom_request(synname + "/label/" + bodyid, "", ConnectionMethod.GET)
    synjson = json.loads(syndata)

    filteredsyn = 0
    unfiltered = 0

    debuglocations = []

    def nearsyn(x,y,z):
        for syn in synjson:
            x2, y2, z2 = syn["Pos"]
            if abs(x2-x) <= synfilter and abs(y2-y) <= synfilter and abs(z2-z) <= synfilter:
                return True
        return False

    # convert to todos
    dviddata = []

    # look for previous annotations
    prev_ann = ns.custom_request(todoname + "/label/" + bodyid, "", ConnectionMethod.GET)
    prevjson = json.loads(prev_ann)
    filteredann = 0
    unfilteredann = 0
    def nearann(x,y,z):
        for ann in prevjson:
            x2, y2, z2 = ann["Pos"]
            if abs(x2-x) <= annfilter and abs(y2-y) <= annfilter and abs(z2-z) <= annfilter:
                return True
        return False

    for data in result:
        x,y,z,x2,y2,z2 = data
        x = int(x)
        y = int(y)
        z = int(z)

        # check if by PSDs
        if nearsyn(x,y,z):
            filteredsyn += 1
            continue
        else:
            unfiltered += 1 

        # check if by other annotations
        if nearann(x,y,z):
            filteredann += 1
            continue
        else:
            unfilteredann += 1 

        # find nearest point if not on body
        window = 1
        nomatch = True
        while window < 128 and nomatch: 
            data = ns.get_labels3D(labelblk, (window, window, window), (z-window/2,y-window/2,x-window/2))
            match = numpy.where(data == int(bodyid))
            if len(match[0] > 0):
                z = match[0][0] + z - window/2
                y = match[1][0] + y - window/2
                x = match[2][0] + x - window/2
                nomatch = False
            window *= 2 

        if nomatch:
            print("NOMATCH!!!")
        else:
            tomerge = {}
            tomerge["Rels"] = None
            tomerge["Kind"] = "Note"
            tomerge["Prop"] = {"action": "to merge", "user": "autotip"}
            tomerge["Pos"] = [int(x),int(y),int(z)]
            debuglocations.append([int(x),int(y),int(z)])
            tomerge["Tags"] = None
            dviddata.append(tomerge)

    # psds filtered
    print("Filtered syn:", filteredsyn)
    print("Unfiltered syn:", unfiltered)
    print("Filtered ann:", filteredann)
    print("Unfiltered ann:", unfilteredann)

    # write todos
    dviddatastr = json.dumps(dviddata)
    ns.custom_request(todoname + "/elements", dviddatastr, ConnectionMethod.POST)
    print(json.dumps(debuglocations))

