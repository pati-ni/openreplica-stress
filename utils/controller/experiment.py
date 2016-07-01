




class OpenReplica(Service):
    def __init__(self):

        Service.__init__(self)
if __name__ == '__main__':

    service = OpenReplica()
    service.run(host="0.0.0.0", port=19080, debug=False)

