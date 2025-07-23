from transformers import ViTFeatureExtractor, BertTokenizer
import torch
import torch.nn as nn

class MultiModalLocator(nn.Module):
    def __init__(self):
        super().__init__()
        self.vit = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
        self.bert = BertTokenizer.from_pretrained('bert-base-uncased')
        self.fusion = nn.TransformerEncoderLayer(d_model=768, nhead=8)
        self.classifier = nn.Linear(768, 1)

    def forward(self, dom_features, screenshot, context_text):
        # Visual pathway
        vis_features = self.vit(screenshot, return_tensors="pt")
        # Text pathway
        text_embeddings = self.bert(context_text, return_tensors="pt")
        # Fusion
        combined = torch.cat([vis_features, text_embeddings, dom_features], dim=1)
        fused = self.fusion(combined)
        return torch.sigmoid(self.classifier(fused)) 