"""
Abstract classes for retrieval and ranking models.

Authors: Hamed Zamani (hazamani@microsoft.com)
"""

from abc import ABC, abstractmethod


class Retrieval(ABC):
	@abstractmethod
	def __init__(self, params):
		"""
		An abstract class for retrieval models.

		Args:
			params(dict): A dict containing some mandatory and optional parameters. 'query_generation' and 'logger' are
			required for all retrieval models.
		"""
		self.params = params
		self.query_generation = self.params['query_generation']

	@abstractmethod
	def retrieve(self, query):
		"""
		This method should retrieve documents for the given query.

		Args:
			query(str): The query string.
		"""
		pass

	def get_results(self, conv_list):
		"""
		This method is the one that should be called. It simply calls the query generation model to generate a query
		from a conversation list and then runs the retrieval model and returns the results.
		Args:
			conv_list(list): List of util.msg.Message, each corresponding to a conversational message from / to the
			user. This list is in reverse order, meaning that the first elements is the last interaction made by user.

		Returns:
			A list of Documents retrieved by the search engine.
		"""
		query = self.query_generation.get_query(conv_list)
		self.params['logger'].info(f'New query: {query}')
		result_list = self.retrieve(query)
		if 'reranker' in self.params:
			return self.params['reranker'].rerank(query, conv_list, result_list, self.params)
		return result_list


class ReRanker(ABC):
	@abstractmethod
	def __init__(self, params):
		"""
		This is an abstract class for a re-ranking model, e.g., learning to rank models.

		Args:
			params(dict): A dict containing some mandatory and optional parameters, such as the hyper-parameters for the
			re-ranking model.
		"""
		self.params = params

	def rerank(self, query, conv_list, result_list, params):
		"""
		This method is called for re-ranking the result_list in response to the query.

		Args:
			query(str): A query generated by a query generation model
			conv_list(list): List of util.msg.Message, each corresponding to a conversational message from / to the
			user. This list is in reverse order, meaning that the first elements is the last interaction made by user.
			result_list(list): A list of Documents retrieved by a first stage retrieval model.
			params(dict): A dict containing some parameters required by the re-ranking model.

		Returns:
			A list of Documents. This list contains a subset of result_list with the highest re-ranking scores.
		"""
		pass


