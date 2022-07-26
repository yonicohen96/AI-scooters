from programio.abstractio import AbstractIO
from programio.consoleio import ConsoleIO
from programio.graphicalio import GraphicIO

from agents.agent import AgentInfo
from agents.staticagent import StaticAgent
from agents.dynamicagent import DynamicAgent
from agents.agentsfactory import AgentsFactory

from data.trafficgenerator import TrafficGenerator
from data.trafficdatatypes import *
from data.featuresdatagenerator import FeaturesDataGenerator, FeaturesData

from simulation.trafficsimulator import TrafficSimulator
from simulation.incomesexpenses import IncomesExpenses

from typing import List, Tuple

import argparse

GET_PROBLEM_PROMPT = "Please type problem to solve from the options below:"
GET_NUMBER_OF_SCOOTER_PROMPT = "Please type number of scooters available:"
GET_NUMBER_OF_NESTS_PROMPT = "Please type number of optional nests:"
GET_INCOMES_FACTOR_PROMPT = "Please type incomes factor:"
GET_EXPENSES_FACTOR_PROMPT = "Please type expenses factor:"
GET_LEARNING_TIME_PROMPT = "Please type learning time (seconds):"
GET_ITERATIONS_NUMBER_DYNAMIC_RUN_PROMPT = "Please enter number of iterations to run" \
                                           " in the end of the learning process:"
GET_AGENT_PROMPT = "Please type agent type:"
GET_DATA_PROMPT = "Please type data choice:"
MIN_NUMBER_OF_SCOOTERS = 1
MAX_NUMBER_OF_SCOOTERS = float("inf")
MIN_NUMBER_OF_NESTS = 1
MAX_NUMBER_OF_NESTS = float("inf")
SEARCH_RADIUS = 40  # todo - get this value as an input? what value to assign?
                    # this value should represent the radius in terms of euclidian
                    #  distance in x,y coordinates of the map (not meters)


class NestsSelector:
    DYNAMIC_AGENT = ["dynamic", "d"]
    STATIC_AGENT = ["static", "s"]
    CUSTOM_DATA = ["custom", "c"]
    DEFAULT_DATA = ["default", "d"]
    CONSOLE_IO = ["console", "c"]
    GRAPHIC_IO = ["graphic", "g"]

    def __init__(self, io: AbstractIO = ConsoleIO()):
        self.io = io
        self.traffic_generator: TrafficGenerator = TrafficGenerator(self.io)
        self.features_data_generator: FeaturesDataGenerator = FeaturesDataGenerator(
            self.io)

    def run(self):
        potential_rides: List[Ride] = self._generate_traffic_data()
        agent_info: AgentInfo = self._get_agent_info(potential_rides)

        if args.agent in NestsSelector.STATIC_AGENT:
            self._run_static_problem(agent_info)
        elif args.agent in NestsSelector.DYNAMIC_AGENT:
            iterations_num: int = int(
                self.io.get_user_numerical_choice(
                    GET_ITERATIONS_NUMBER_DYNAMIC_RUN_PROMPT, 0, float("inf")))
            self._run_dynamic_problem(agent_info, iterations_num)

    def _generate_traffic_data(self) -> List[Ride]:
        # return the data requested:
        if args.data in NestsSelector.DEFAULT_DATA:
            return self.traffic_generator.get_default_data()
        elif args.data in NestsSelector.CUSTOM_DATA:
            return self.traffic_generator.get_custom_data()

    def _get_agent_info(self, potential_rides: List[Ride]):

        traffic_simulator: TrafficSimulator = TrafficSimulator(potential_rides,
                                                               SEARCH_RADIUS)
        incomes_factor: float = self.io.get_user_numerical_choice(
            GET_INCOMES_FACTOR_PROMPT, 0, float("inf"))
        expenses_factor: float = self.io.get_user_numerical_choice(
            GET_EXPENSES_FACTOR_PROMPT, 0, float("inf"))
        incomes_expenses: IncomesExpenses = IncomesExpenses(incomes_factor,
                                                            expenses_factor)
        features_data: FeaturesData = self.features_data_generator. \
            generate_features_data()
        learning_time = int(
            self.io.get_user_numerical_choice(GET_LEARNING_TIME_PROMPT, 0,
                                              float("inf")))
        nests_num: int = int(self.io.get_user_numerical_choice(
            GET_NUMBER_OF_NESTS_PROMPT, MIN_NUMBER_OF_NESTS, MAX_NUMBER_OF_NESTS))
        optional_nests: List[Point] = self. \
            traffic_generator.get_random_nests_locations(nests_num)
        scooters_num: int = int(self.io.get_user_numerical_choice(
            GET_NUMBER_OF_SCOOTER_PROMPT, MIN_NUMBER_OF_SCOOTERS,
            MAX_NUMBER_OF_SCOOTERS))

        return AgentInfo(traffic_simulator, incomes_expenses, features_data,
                         learning_time, optional_nests, scooters_num)

    def _run_static_problem(self, agent_info: AgentInfo):

        # get agent:
        agent_chosen: str = self.io.get_user_discrete_choice(
            GET_AGENT_PROMPT, AgentsFactory.get_static_agent_legal_values())
        agent: StaticAgent = AgentsFactory.build_static_agent(agent_chosen,
                                                              agent_info)

        # get result:
        result: Tuple[List[NestAllocation], float] = agent.spread_scooters()
        spread_points: List[NestAllocation] = result[0]
        revenue: float = result[1]

        # show result
        self._show_static_results(agent, spread_points, revenue)

    def _run_dynamic_problem(self, agent_info: AgentInfo, iterations_num: int):

        # get agent:
        agent_chosen: str = self.io.get_user_discrete_choice(
            GET_AGENT_PROMPT, AgentsFactory.get_dynamic_agent_legal_values())
        agent: DynamicAgent = AgentsFactory.build_dynamic_agent(agent_chosen,
                                                                agent_info)

        # learn:
        agent.learn()

        # show result:
        avg_revenue: float = agent.get_average_revenue(iterations_num)
        self._show_dynamic_results(agent, avg_revenue)

    def _show_static_results(self, agent: StaticAgent,
                             spread_points: List[NestAllocation], revenue: float):
        self.io.show_value("revenue:", revenue)
        self.io.confirm_and_continue()
        self.io.show_spread(spread_points)
        # todo - after building the simulator, think of a way to show a simulation,
        #        maybe in the simulator use an option of simulation for visualization
        #        and use "yield" to get stated during the simulation
        # start_points: List[Point] = agent.agent_info.traffic_simulator.\
        #     get_scooters_location_from_nests_spread(spread_points)

    def _show_dynamic_results(self, agent: DynamicAgent, avg_revenue: float):
        self.io.show_value("average revenue:", avg_revenue)
        self.io.confirm_and_continue()
        # todo - think of how to present the result of the dynamic agent after
        # building the simulator
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--io",
                        default='c',
                        help="The input/output interface of the program",
                        choices=NestsSelector.CONSOLE_IO + NestsSelector.GRAPHIC_IO)
    parser.add_argument("-a",
                        "--agent",
                        default='d',
                        help="The type of agent",
                        choices=NestsSelector.DYNAMIC_AGENT + NestsSelector.STATIC_AGENT)
    parser.add_argument("-d",
                        "--data",
                        default='d',
                        help="The type of data",
                        choices=NestsSelector.DEFAULT_DATA+NestsSelector.CUSTOM_DATA)
    args = parser.parse_args()
    io = GraphicIO() if args.io in NestsSelector.GRAPHIC_IO else ConsoleIO()
    ns = NestsSelector()
    ns.run()
