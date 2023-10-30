from scapy.all import ARP, Ether, srp

def scan_local_network(ip_range):
    # Создаем ARP-пакет для запроса MAC-адресов в указанном IP-диапазоне
    arp = ARP(pdst=ip_range)
    # Создаем Ethernet-кадр для отправки ARP-пакета
    ether = Ether(dst="eth0")
    # Комбинируем Ethernet-кадр и ARP-пакет
    packet = ether/arp

    # Отправляем пакет и получаем ответы
    result = srp(packet, timeout=3, verbose=False)[0]

    # Собираем IP-адреса из ответов
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

if __name__ == "__main__":
    # Указываем IP-диапазон для сканирования (например, "192.168.1.1/24")
    ip_range = input("Введите IP-диапазон для сканирования (например, '192.168.1.1/24'): ")

    # Вызываем функцию сканирования и выводим результат
    devices = scan_local_network(ip_range)
    print("Список подключенных устройств в локальной сети:")
    print("IP адрес\t\tMAC адрес")
    for device in devices:
        print(f"{device['ip']}\t\t{device['mac']}")
