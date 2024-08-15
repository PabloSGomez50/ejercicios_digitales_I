import click
import serial
import serial.tools.list_ports
import os

SERIAL_TIMEOUT = os.getenv("SERIAL_TIMEOUT", 3) # Seconds
SERIAL_BAUDRATE = os.getenv("SERIAL_BAUDRATE", 9600)

def list_available_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()
    available_ports = [
        f'{port.device.replace("COM", ""):0>2}-{port.device}:\t{port.description}' 
        for port in ports]
    return sorted(available_ports)

def open_connection(port, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT):
    """
    Open a connection to a specified serial port.
    https://pyserial.readthedocs.io/en/latest/pyserial_api.html
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        if ser.is_open:
            click.echo(f"Connection to {port} opened successfully.")
        return ser
    except serial.SerialException as e:
        click.echo(f"Failed to open connection: {e}")
        return None

def close_connection(ser):
    """Close the serial connection."""
    if ser and ser.is_open:
        ser.close()
        click.echo("Connection closed.")
    else:
        click.echo("Connection already closed or not established.")

def send_data(ser, content: str):
    """send serial data."""
    if ser and ser.is_open:
        ser.write(content.encode('utf-8'))
        response = ser.readline().decode('utf-8').strip()
        return response
    else:
        click.echo("Connection not open.")
        return None
    
def get_driving_values():
    """ Obtener los valores del f1 a partir de la screenshot"""
    
    return 0, 0

@click.group()
def cli():
    """Simple CLI for serial communication."""
    pass

@cli.command()
def ports():
    """List all available serial ports."""
    ports = list_available_ports()
    if not ports:
        click.echo("No available ports found.")
    else:
        click.echo("Available ports:")
        for port in ports:
            click.echo(port)


@cli.command()
@click.option('--port', prompt='Serial port', help='The serial port to connect to.')
@click.option('--baudrate', default=SERIAL_BAUDRATE, help='The baud rate for the serial connection.')
@click.option('--timeout', default=SERIAL_TIMEOUT, help='The timeout for the serial connection.')
def play_f1(port, baudrate, timeout):
    """Open a connection to a specified serial port."""
    ser = open_connection(port, baudrate, timeout)
    while ser:
        click.echo("Connection successful!")
        velocity, gear = get_driving_values()
        if velocity and gear: 
            response = send_data(ser, f'{velocity}, {gear}\n')
        click.echo(f"Response from device: {response}")
        close_connection(ser)

if __name__ == '__main__':
    cli()
