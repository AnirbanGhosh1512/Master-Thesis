"""
Production Factory product making example

Scenario:
  A production factory has a limited number of production modules(here it is 4) that share a common
  carrier. materials arrives to the carrier, request one by one production modules(not asynchronous)
  it is a continues process though some modules can be skipped.

"""
import itertools
import random
import copy
import simpy


RANDOM_SEED = 42
FACTORY_SIZE = 1
PRODUCTION_MODULE_SIZE = 4     # based on area
THRESHOLD = [10, 5, 15, 23]    # Threshold for calling carrier after it is done job (in time t as %)
PRODUCTION_MODULE_STEPS = ['1T', '2T', '3T', '4T']
CARRIER_SIZE = 1            # weight to carry
CARRIER_VELOCITY = 2       # meter/second
SIM_TIME = 1000            # Simulation time in seconds
T_INTER = [30, 300]        # Create a car every [min, max] seconds



#def car(name, env, production_modules, carrier):
def production_control(name, env, production_factory, production_modules):
    """The product needs 4 production steps, which can be performed by the production modules.
    Every production module has its own processing time t. The production module operates with a
    carrier which can only move in circles. The carrier can always carry only one product which
    is removed by the production modules while they are processed, and returned to the carrier
    when they are finished. After the product has completed with all necessary production steps,
    it needs to be brought to the product removal where it is removed from production.

    """

    print('%s arriving at production factory at %.1f' % (name, env.now))
    with production_factory.request() as req:
        # Request for production factory
        yield req
        for i in itertools.count():
            yield env.timeout(random.randint(*T_INTER))
            start = env.now
            print('Steps of production %d' % i)
            # Get the steps required
            steps = random.sample(PRODUCTION_MODULE_STEPS, len(PRODUCTION_MODULE_STEPS))
            # Sometimes steps 2 and 4 are not required.
            if i==3 or i==5:
                steps = [step.replace('2T', '2F') for step in steps]
                steps = [step.replace('4T', '4F') for step in steps]
                # steps.remove(2)
                # steps.remove(4)
            # Make the list as a cycle as carrier moves circular manner.
            steps_circular = itertools.cycle(steps)
            # if len(steps) == 1:
            #     PRODUCTION_MODULE_STEPS.remove(2)
            #     PRODUCTION_MODULE_STEPS.remove(4)
            # Run the carrier on cycle.
            module_checked = []
            # check if 2F and 4F are in modules.
            module_negetive = []
            for pm_steps in PRODUCTION_MODULE_STEPS:
                if pm_steps in module_checked:
                    continue
                else:
                    iteration = 1
                    while iteration < len(steps) + 1:
                        item = next(steps_circular)
                        if pm_steps == item:
                            duration = THRESHOLD[iteration - 1]
                            yield env.timeout(duration)
                            yield env.timeout(CARRIER_VELOCITY)
                            module_checked.append(pm_steps)
                            if '2F' in steps:
                                if pm_steps == '1T':
                                    pm_steps = '3T'
                                    module_negetive.append('1T')
                                elif pm_steps == '3T':
                                    module_negetive.append('3T')
                            else:
                                if pm_steps == '1T':
                                    pm_steps = '2T'
                                elif pm_steps == '2T':
                                    pm_steps = '3T'
                                elif pm_steps == '3T':
                                    pm_steps = '4T'
                            iteration = iteration + 1
                        else:
                            if pm_steps == 1 and iteration == 1:
                                iteration = iteration + 1
                                continue
                            else:
                                yield env.timeout(CARRIER_VELOCITY)
                            iteration = iteration + 1
                if '2F' in steps:
                    if '1T' and '3T' in module_negetive:
                        break


            print('%s finished product in %.1f seconds.' % (name,
                                                              env.now - start))


def carrier(env, production_factory, production_modules):
    """Generate carrier that arrive at the production factory."""
    yield env.timeout(random.randint(*T_INTER))
    env.process(production_control('Carrier', env, production_factory, production_modules))


# Setup and start the simulation
print('Production Factory simulation')
random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()
production_factory = simpy.Resource(env, 1)
production_modules = simpy.Container(env, FACTORY_SIZE, init=FACTORY_SIZE)
#env.process(production_factory_control(env, production_modules))
env.process(carrier(env, production_factory, production_modules))


# Execute!
env.run(until=SIM_TIME)