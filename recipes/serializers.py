from rest_framework import serializers

from .models import CookingMethod, CookingStepInstruction, Equipment, Ingredient, Recipe, RecipeImage, RecipeIngredient, Unit, Cuisine, Occasion, Meal
from recipes.utils.language import LanguageMixin

class IngredientSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    allergen = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'allergen', 'category']

    def get_name(self, obj):
        return self.get_localized_field(obj)
    
    def get_allergen(self, obj):
        return self.get_localized_field(obj)
            
    def get_category(self, obj):
        return self.get_localized_field(obj)

class UnitSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Unit
        fields = ['type_shoping_valid', 'name']

    def get_name(self, obj):
        return self.get_localized_field(obj)
        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    unit = UnitSerializer()
    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'ingredient', 'unit']

class CookingStepInstructionSerializer(LanguageMixin, serializers.ModelSerializer):
    instruction = serializers.SerializerMethodField()
    class Meta:
        model = CookingStepInstruction
        fields = ['step_number', 'instruction']

    def get_instruction(self, obj):
        return self.get_localized_field(obj)
    
class ImageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RecipeImage
        fields = ['thumbnail_url', 'image_url']

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:  # Make sure the field exists
            return self.context['request'].build_absolute_uri(obj.thumbnail.url)
        return None

    def get_image_url(self, obj):
        if obj.image:  # Make sure the field exists
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class EquipmentSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Equipment
        fields = ['name']
    
    def get_name(self, obj):
        return self.get_localized_field(obj)

class CookingMethodSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CookingMethod
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)

class CuisineSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Cuisine
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)
    
class OccasionSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Occasion
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)

class MealSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Meal
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)

class RecipeSerializer(LanguageMixin, serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)
    instructions = CookingStepInstructionSerializer(many=True)
    equipment = EquipmentSerializer(many = True)
    cooking_methods = CookingMethodSerializer(many = True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cuisines = CuisineSerializer(many=True)
    occasions = OccasionSerializer(many=True)
    meals = MealSerializer(many=True)
    images = ImageSerializer(many=True) 
    created_time = serializers.SerializerMethodField()      
    modified_time = serializers.SerializerMethodField()      

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'created_time',
            'modified_time',
            'cuisines',
            'occasions',
            'meals',
            'equipment',
            'cooking_methods',
            'servings',
            'instructions',
            'recipe_ingredients',
            'cooking_time',
            'calculated_total_price',
            'images',
        ]


    def get_title(self, obj) -> str:
        return self.get_localized_field(obj.title)
    
    def get_description(self, obj) -> str:
        return self.get_localized_field(obj.description)
    
    def get_created_time(self, obj):
        return obj.created_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    def get_modified_time(self, obj):
        return obj.modified_time.strftime("%Y-%m-%d %H:%M:%S %Z")

class BaseRecipeSerializer(LanguageMixin, serializers.HyperlinkedModelSerializer):
    title = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)

    def get_title(self, obj):
        return self.get_localized_field(obj.title)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang_param = self.context['request'].GET.get('lang')

        if 'url' in data and lang_param:
            modified_url = data['url'] + f'?lang={lang_param}'
            data['url'] = modified_url
        return data

class RecipeMinimalSerializer(BaseRecipeSerializer):
    class Meta:
        model = Recipe
        fields = ['url', 'id', 'title', 'images']

class RecipeSearchPageSerializer(BaseRecipeSerializer):
    class Meta:
        model = Recipe
        fields = ['url', 'id', 'title', 'cooking_time', 'calculated_total_price', 'images']
