from pykeen.triples import TriplesFactory
from typing import List, Dict

import torch
import numpy as np


class SimilarityPredictor:
    def __init__(self):
        self.model = torch.load(
            'data/trained_model.pkl',
            map_location="cpu",
            weights_only=False
        )
        self.triples_factory = TriplesFactory.from_path(
            'data/dataset_train.tsv.gz'
        )
        self.same_as_relation_id = self.triples_factory.relation_to_id['http://www.w3.org/2002/07/owl#sameAs']

    def _is_valid_property_index(self, property_index: int) -> bool:
        return property_index in self.triples_factory.entity_to_id.values()

    def predict_top_n_similar_properties(
        self,
        property_index: int,
        top_n: int
    ) -> List[Dict[str, float]]:
        if not self._is_valid_property_index(property_index):
            return f"Invalid property index: {property_index}"

        head_idx = [property_index]
        relations_idx = [self.same_as_relation_id]

        tensor = torch.tensor(list(zip(head_idx,relations_idx)))
        scores = self.model.score_t(tensor).cpu().detach().numpy()[0]
        similar_properties_indices = np.argsort(scores)[1: top_n + 1]
        
        return {
            "property_index": property_index,
            "similar_properties": [
                {
                    "property_index": int(index),
                    "similarity_score": float(scores[index])
                }   for index in similar_properties_indices
            ]
        }