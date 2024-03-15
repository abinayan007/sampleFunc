import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.FUNCTION)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
# import os

# import azure.functions as func
# import logging
# import json, socket, ssl, sys, time, zlib, datetime
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# #TCP socket connection creds
# username = os.environ["user_name"]
# apikey = os.environ["apikey"]
# compression = None        # set to "deflate", "decompress", or "gzip" to enable compression
# servername = os.environ["servername"]

# # Define Azure Blob Storage connection string,container name and blob name
# connection_string = os.environ["connection_string"]
# container_name = os.environ["container_name"]
# blob_name = os.environ["blob_name"]

# class InflateStream:
#     "A wrapper for a socket carrying compressed data that does streaming decompression"

#     def __init__(self, sock, mode):
#         self.sock = sock
#         self._buf = bytearray()
#         self._eof = False
#         if mode == 'deflate':     # no header, raw deflate stream
#             self._z = zlib.decompressobj(-zlib.MAX_WBITS)
#         elif mode == 'compress':  # zlib header
#             self._z = zlib.decompressobj(zlib.MAX_WBITS)
#         elif mode == 'gzip':      # gzip header
#             self._z = zlib.decompressobj(16 | zlib.MAX_WBITS)
#         else:
#             raise ValueError('unrecognized compression mode')

#     def _fill(self):
#         rawdata = self.sock.recv(8192)
#         if len(rawdata) == 0:
#             self._buf += self._z.flush()
#             self._eof = True
#         else:
#             self._buf += self._z.decompress(rawdata)

#     def readline(self):
#         newline = self._buf.find(b'\n')
#         while newline < 0 and not self._eof:
#             self._fill()
#             newline = self._buf.find(b'\n')

#         if newline >= 0:
#             rawline = self._buf[:newline +1]
#             del self._buf[:newline +1]
#             return rawline.decode('ascii')

#         # EOF
#         return ''

# # function to parse JSON data:
# def parse_json( str ):
#     try:
#         # parse all data into dictionary decoded:
#         decoded = json.loads(str)
#         print(decoded)
#         logging.info(decoded)

#         # compute the latency of this message:
#         clocknow = time.time()
#         diff = clocknow - int(decoded['pitr'])
#         print("diff = {0:.2f} s\n".format(diff))
#     except (ValueError, KeyError, TypeError):
#         logging.error("TCP connection message parsing error. ", sys.exc_info()[0])
#         print("JSON format error: ", sys.exc_info()[0])

#     return;

# # Disable hostname verification by providing a custom hostname verifier function. Only for dev purpose
# def verify_host(hostname, ssl_context):
#     return True

# def main(precom, postcom=""):
#     # Create socket
#     sock = socket.socket(socket.AF_INET)
#     # Create a SSL context with the recommended security settings for client sockets, including automatic certificate verification
#     context = ssl.create_default_context()
#     # bypassing hostname,SSL cert check for dev purpose
#     context.check_hostname = False
#     context.verify_mode = ssl.CERT_NONE
#     context.hostname_check_callback = verify_host
#     # the folowing line requires Python 3.7+ and OpenSSL 1.1.0g+ to specify minimum_version
#     context.minimum_version = ssl.TLSVersion.TLSv1_2

#     ssl_sock = context.wrap_socket(sock, server_hostname=servername)
#     print("Connecting...")
#     ssl_sock.connect((servername, 1501))
#     print("Connection succeeded")

#     # ===========================================================COMMAND======================================
#     # build the initiation command:
#     initiation_command = precom + " username {} password {} airport_filter KBOS".format(username, apikey) + postcom

#     if compression is not None:
#         initiation_command += " compression " + compression

#     # send initialization command to server:
#     initiation_command += "\n"
#     if sys.version_info[0] >= 3:
#         ssl_sock.write(bytes(initiation_command, 'UTF-8'))
#     else:
#         ssl_sock.write(initiation_command)

#     # return a file object associated with the socket
#     if compression is not None:
#         file = InflateStream(sock=ssl_sock, mode=compression)
#     else:
#         file = ssl_sock.makefile('r')

#     # Create a BlobServiceClient object which will be used to create a container client
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     # Create a ContainerClient object which will be used to upload a blob
#     container_client = blob_service_client.get_container_client(container_name)
#     # Create a new blob name based on the current datetime
#     blob_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + " ApFil " + precom + ".txt"
#     # create a blob client to Upload data to the new blob
#     blob_client = container_client.get_blob_client(blob_name)

#     #used to collect responses received according to the count
#     concat = ''
#     # use "while True" for no limit in messages received.
#     # Used to control amount of messages to be collected
#     count = int(os.environ["count"])
#     while (count > 0):
#         try:
#             # read line from file:
#             inline = file.readline()
#             concat += inline
#             if inline == '':
#                 # EOF
#                 break

#             # parse the line
#             parse_json(inline)
#             count = count - 1
#         except socket.error as e:
#             logging.error("socket error. connection failed ", sys.exc_info()[0])
#             print('Connection fail', e)
#             print(traceback.format_exc())

#     # Upload data to the blob
#     blob_client.upload_blob(concat, overwrite=True)

#     # close the SSLSocket, will also close the underlying socket
#     ssl_sock.close()


# @app.route(route="http_trigger")
# def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function triggered')

#     try:
#         #getting the request body
#         req_body = req.get_json()
#         # retrieving the pre and post command. Precomand is mandatory. Post is optional.
#         pre_com = req_body.get("precom")
#         post_com = req_body.get("postcom")

#     except (ValueError, TypeError, json.JSONDecodeError):
#         logging.error("Bad Request body ", sys.exc_info()[0])
#         return func.HttpResponse(
#             "This HTTP triggered function failed to excute. Bad Request body.Failed to process request body.",
#             status_code=400
#         )
#     else:

#         try:

#             if pre_com:
#                 if post_com:

#                     main(pre_com, post_com)
#                 else:
#                     main(pre_com)

#             else:
#                 logging.error("Bad Request body.Absence of expected properties ", sys.exc_info()[0])
#                 #No precommand exist. Hence cannot process the request
#                 return func.HttpResponse(
#                     "This HTTP triggered function executed successfully. Bad Request. Absence of expected properties",
#                     status_code=400
#                 )
#         except Exception as e:
#             logging.error("Internal Server error ",sys.exc_info()[0])
#             print("Internal Server error ", sys.exc_info()[0])
#             return func.HttpResponse(
#                 "This HTTP triggered function failed to excute. Internal Server Error.",
#                 status_code=500
#             )

#         else:
#             logging.info("This HTTP triggered function executed successfully. Data ingested successfully")
#             #successfully ingested the data
#             return func.HttpResponse(
#                 "This HTTP triggered function executed successfully. Data ingested successfully",
#                 status_code=200
#             )



