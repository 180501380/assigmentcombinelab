"""new table from assigment project

Revision ID: f6fa1a930675
Revises: ae346256b650
Create Date: 2019-04-21 11:35:47.100814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6fa1a930675'
down_revision = 'ae346256b650'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('advertisement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('advertisement_link', sa.String(length=4000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_country_name'), 'country', ['name'], unique=True)
    op.create_table('cusine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('food',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_google_link', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menu_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('postlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menu_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('link', sa.String(length=150), nullable=False),
    sa.Column('menu_category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['menu_category_id'], ['menu_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('cusine_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('intro', sa.String(length=500), nullable=True),
    sa.Column('spending_per_head', sa.Integer(), nullable=True),
    sa.Column('open_hour', sa.Integer(), nullable=True),
    sa.Column('closing_hour', sa.Integer(), nullable=True),
    sa.Column('working_day', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['cusine_id'], ['cusine.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_restaurant_name'), 'restaurant', ['name'], unique=True)
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telephone', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurantfeature',
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], )
    )
    op.create_table('restaurantfood',
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('food_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], )
    )
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photo_link', sa.String(length=4000), nullable=True),
    sa.Column('number_of_like', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('post', sa.Column('advertisement_id', sa.Integer(), nullable=True))
    op.add_column('post', sa.Column('number_of_like', sa.Integer(), nullable=True))
    op.add_column('post', sa.Column('restaurant_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'advertisement', ['advertisement_id'], ['id'])
    op.create_foreign_key(None, 'post', 'restaurant', ['restaurant_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'restaurant_id')
    op.drop_column('post', 'number_of_like')
    op.drop_column('post', 'advertisement_id')
    op.drop_table('photo')
    op.drop_table('restaurantfood')
    op.drop_table('restaurantfeature')
    op.drop_table('contact')
    op.drop_index(op.f('ix_restaurant_name'), table_name='restaurant')
    op.drop_table('restaurant')
    op.drop_table('menu_item')
    op.drop_table('postlist')
    op.drop_table('menu_category')
    op.drop_table('location')
    op.drop_table('food')
    op.drop_table('feature')
    op.drop_table('cusine')
    op.drop_index(op.f('ix_country_name'), table_name='country')
    op.drop_table('country')
    op.drop_table('advertisement')
    # ### end Alembic commands ###
