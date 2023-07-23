import os
import argparse
import selectors
import socket
import serial
import signal

# abort flag (global)
g_abort_service = False

# wakeup pipe (global)
g_wakeup_write = None

# sigint handler
def sigint_handler(signum, frame):
  print("CTRL-C is pressed. Stopping the service.")
  global g_abort_service
  g_abort_service = True
  global g_wakeup_write
  os.write(g_wakeup_write, b'1')

# serial event handler
def serial_event_handler(key, mask, udp_socket_tx, remote_address):
  data = key.fileobj.read()
  udp_socket_tx.sendto(data, remote_address)
  #print(f"Received {len(data)} bytes from serial port.")

# udp event handler
def udp_event_handler(key, mask, serial_port):
  data, addr = key.fileobj.recvfrom(1024)
  serial_port.write(data)
  #print(f"Received {len(data)} bytes from UDP.")

# service loop
def run_service(remote_ip, remote_port, listen_port, serial_device, serial_baudrate):

  # open serial port
  with serial.Serial(serial_device, serial_baudrate,
                     bytesize = serial.EIGHTBITS,
                     parity = serial.PARITY_NONE,
                     stopbits = serial.STOPBITS_ONE,
                     timeout = 120,
                     xonxoff = False,
                     rtscts = False,
                     dsrdtr = False ) as serial_port:

    # remote address
    remote_address = (remote_ip, remote_port)

    # udp socket for tx
    udp_socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # udp socket for rx
    udp_socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket_rx.bind(('0.0.0.0', listen_port))

    # pipe for select loop breaking
    wakeup_read, wakeup_write = os.pipe()

    # set sigterm handler
    global g_abort_service
    g_abort_service = False
    global g_wakeup_write
    g_wakeup_write = wakeup_write
    signal.signal(signal.SIGINT, sigint_handler)

    # IO selector
    selector = selectors.DefaultSelector()
    selector.register(serial_port, selectors.EVENT_READ, serial_event_handler)
    selector.register(udp_socket_rx, selectors.EVENT_READ, udp_event_handler)
    selector.register(wakeup_read, selectors.EVENT_READ)

    print(f"Started. (remote={remote_ip}:{remote_port}, listen_port={listen_port}, serial_device={serial_device}, baudrate={serial_baudrate})")

    try:
      while g_abort_service is False:
        events = selector.select()
        for key, mask in events:
          if key.fileobj == serial_port:
            callback = key.data
            callback(key, mask, udp_socket_tx, remote_address)
          elif key.fileobj == udp_socket_rx:
            callback = key.data
            callback(key, mask, serial_port)
          elif key.fileobj == wakeup_read:
            os.read(wakeup_read, 1)
    except Exception as e:
        print(e)
    finally:
      selector.unregister(serial_port)
      selector.unregister(udp_socket_rx)
      selector.close()
      serial_port.close()
      udp_socket_rx.close()
      udp_socket_tx.close()
      os.close(wakeup_read)
      os.close(wakeup_write)

    print("Stopped.")

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("remote_ip", help="remote serialudp IP address")
  parser.add_argument("remote_port", help="remote serialudp port number", type=int)
  parser.add_argument("-l","--listen_port", help="listen port number (default:6830)", type=int, default=6830)
  parser.add_argument("-d","--device", help="serial device name (default:/dev/ttyUSB0)", default='/dev/ttyUSB0')
  parser.add_argument("-s","--baudrate", help="baud rate (default:9600)", type=int, default=9600)
 
  args = parser.parse_args()

  return run_service(args.remote_ip, args.remote_port, args.listen_port, args.device, args.baudrate)

if __name__ == "__main__":
  main()
