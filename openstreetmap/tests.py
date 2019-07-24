# -*- coding: utf-8 -*-

from django.test import TestCase
from django.urls import reverse

from .views import QueryOpenStreetMapReverse, QueryOpenStreetMapSearch

class TestGeocodingViews(TestCase):
	"""Teste de views do sistema de geocodificação"""

	def setUp(self):
		self.search_url = reverse('osm:osm-search')
		self.reverse_url = reverse('osm:osm-reverse')

	def test_url_reverse(self):
		self.assertEqual(self.search_url, '/search/')
		self.assertEqual(self.reverse_url, '/reverse/')

	def test_url_get_search_response_error(self):
		response = self.client.get(self.search_url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['location'], "Parameter is missing")

	def test_url_get_reverse_response_error(self):
		response = self.client.get(self.reverse_url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['lat'], "Parameter is missing")

		response = self.client.get(self.reverse_url, data={"lat": 10})
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['lon'], "Parameter is missing")

	def test_url_post_search_response_error(self):
		response = self.client.post(self.search_url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['location'], "Parameter is missing")

	def test_url_post_reverse_response_error(self):
		response = self.client.post(self.reverse_url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['lat'], "Parameter is missing")

		response = self.client.post(self.reverse_url, data={"lat": 10})
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['lon'], "Parameter is missing")

	def tearDown(self):
		pass
