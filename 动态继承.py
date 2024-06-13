class DynamicInheritanceMeta(type):
    def __call__(cls, *args, **kwargs):
        # 根据instance_type属性的值选择基类
        instance_type = kwargs.pop('instance_type', None)

        if instance_type == 'A':
            base_class = BaseClassA
        elif instance_type == 'B':
            base_class = BaseClassB
        else:
            raise ValueError('Invalid instance type')

        # 动态创建类
        instance_class = type('InstanceClass', (base_class, cls), {})
        instance = super().__call__(*args, **kwargs)

        return instance

class BaseClassA:
    def __init__(self):
        self.type = 'A'

class BaseClassB:
    def __init__(self):
        self.type = 'B'

class DynamicInheritanceExample(metaclass=DynamicInheritanceMeta):
    def __init__(self, *args, **kwargs):
        self.instance_type = kwargs.get('instance_type', 'A')

    def hello(self):
        print(f'Hello from {self.instance_type}')

if __name__ == '__main__':
    example = DynamicInheritanceExample(instance_type='A')
    example.hello()