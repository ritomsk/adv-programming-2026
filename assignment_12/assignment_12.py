from abc import ABC, abstractmethod
from dataclasses import dataclass


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order_data: dict) -> None:
        pass

class Order(ABC):
    @abstractmethod
    def get_total(self) -> float:
        pass
    
    @abstractmethod
    def get_summary(self) -> dict:
        pass

@dataclass
class RegularOrder(Order):
    item_name: str
    price: float

    def get_total(self) -> float:
        return self.price

    def get_summary(self) -> dict:
        return {"type": "Regular", "item": self.item_name, "total": self.get_total()}

@dataclass
class DiscountedOrder(Order):
    item_name: str
    price: float
    discount_amount: float

    def get_total(self) -> float:
        return max(0.0, self.price - self.discount_amount)

    def get_summary(self) -> dict:
        return {"type": "Discounted", "item": self.item_name, "total": self.get_total()}

class CreditCardPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"[Payment] Connecting to Stripe... Processed ${amount:.2f} via Credit Card.")
        return True

class UPIPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"[Payment] Connecting to UPI Gateway... Processed ${amount:.2f} via UPI.")
        return True

class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Notification - EMAIL] {message}")

class SMSNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Notification - SMS] {message}")

class DatabaseRepository(OrderRepository):
    def save(self, order_data: dict) -> None:
        print(f"[Storage] INSERT INTO orders ... Data: {order_data}")

class FileRepository(OrderRepository):
    def save(self, order_data: dict) -> None:
        print(f"[Storage] Appending to orders.json ... Data: {order_data}")

class OrderService:
    def __init__(self, 
                 payment_processor: PaymentProcessor, 
                 notifier: Notifier, 
                 repository: OrderRepository):
        self.payment_processor = payment_processor
        self.notifier = notifier
        self.repository = repository

    def place_order(self, order: Order) -> None:
        print("\n--- Starting Order Processing ---")
        
        amount = order.get_total()
        
        is_successful = self.payment_processor.process_payment(amount)
        
        if not is_successful:
            print("[Error] Payment failed. Order cancelled.")
            return

        order_data = order.get_summary()
        self.repository.save(order_data)
        
        self.notifier.send(f"Success! Your order for '{order_data['item']}' has been confirmed.")
        print("--- Order Processing Complete ---")

if __name__ == "__main__":
    
    regular_order = RegularOrder(item_name="Wireless Mouse", price=25.00)
    
    service_1 = OrderService(
        payment_processor=CreditCardPayment(),
        notifier=EmailNotifier(),
        repository=DatabaseRepository()
    )
    service_1.place_order(regular_order)

    discounted_order = DiscountedOrder(item_name="Mechanical Keyboard", price=100.00, discount_amount=15.00)
    
    service_2 = OrderService(
        payment_processor=UPIPayment(),
        notifier=SMSNotifier(),
        repository=FileRepository()
    )
    service_2.place_order(discounted_order)