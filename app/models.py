from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship, declarative_base
from .database import Base


class ItemDatabaseUser(Base):
    __tablename__ = "users"

    id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    email = Column(mysql.VARCHAR(length=50), nullable=False, unique=True)
    password = Column(mysql.VARCHAR(length=255), nullable=False)
    created_at = Column(mysql.DATETIME(), nullable=False,
                        server_default=text('NOW()'))

class Vote(Base):
    __tablename__ = "votes"

    item_id = Column(mysql.INTEGER, ForeignKey(
        "item.item_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(mysql.INTEGER, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True, nullable=False)


class MediaFormat(Base):
    __tablename__ = "media_format"

    format_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    format_name = Column(mysql.VARCHAR(length=10))


class Genre(Base):
    __tablename__ = "genre"

    genre_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    genre_name = Column(mysql.VARCHAR(length=20))


class Country(Base):
    __tablename__ = "country"

    country_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    country_name = Column(mysql.VARCHAR(length=15))


class Condition(Base):
    __tablename__ = "item_condition"

    condition_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    condition_description = Column(mysql.VARCHAR(length=15))

class Region(Base):
    __tablename__ = "region"

    region_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    region_name = Column(mysql.VARCHAR(length=15))


class Subtitles(Base):
    __tablename__ = "subtitles"

    subtitle_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    subtitle_name = Column(mysql.VARCHAR(length=15))


class Packaging(Base):
    __tablename__ = "packaging"

    packaging_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    packaging_name = Column(mysql.VARCHAR(length=15))

class ShippingCosts(Base):
    __tablename__ = "shipping_costs"

    shipping_costs_id = Column(mysql.INTEGER, primary_key=True, nullable=False)
    shipping_price = Column(mysql.DECIMAL(
        precision=4, scale=2), nullable=False)
    shipping_description = Column(mysql.VARCHAR(length=20), nullable=False)

class Item(Base):
    __tablename__ = "item"

    item_id = Column(mysql.INTEGER(), primary_key=True, nullable=False)
    item_description = Column(mysql.VARCHAR(length=60), nullable=True)
    item_format = Column(mysql.INTEGER(), ForeignKey(
        "media_format.format_id", ondelete="SET NULL"), nullable=True)
    item_genre = Column(mysql.INTEGER(), ForeignKey(
        "genre.genre_id", ondelete="SET NULL"), nullable=True)
    item_country = Column(mysql.INTEGER(), ForeignKey(
        "country.country_id", ondelete="SET NULL"), nullable=True)
    item_region = Column(mysql.INTEGER(), ForeignKey(
        "region.region_id", ondelete="SET NULL"), nullable=True)
    item_subtitles = Column(mysql.INTEGER(),  ForeignKey(
        "subtitles.subtitle_id", ondelete="SET NULL"), nullable=True)
    item_packaging = Column(mysql.INTEGER(),  ForeignKey(
        "packaging.packaging_id", ondelete="SET NULL"), nullable=True)
    item_slipcover = Column(mysql.TINYINT(), nullable=True, default=0)
    item_condition = Column(mysql.INTEGER(), ForeignKey(
        "item_condition.condition_id", ondelete="SET NULL"), nullable=True)
    item_condition_comment = Column(mysql.VARCHAR(length=255), nullable=True)
    item_images = Column(mysql.VARCHAR(length=255), nullable=True)
    item_price = Column(mysql.DECIMAL(precision=5, scale=2), nullable=True)
    item_shipping = Column(mysql.INTEGER(), ForeignKey(
        "shipping_costs.shipping_costs_id", ondelete="SET NULL"), nullable=True)
    item_huuto_id = Column(mysql.INTEGER(), nullable=True)
    item_huuto_text = Column(mysql.VARCHAR(length=1024), nullable=True)
    item_huuto_endtime = Column(mysql.DATETIME(), nullable=True)
    item_modified = Column(mysql.TINYINT(), nullable=True, default=0)
    #owner_id = Column(mysql.INTEGER(), ForeignKey(
    #    "users.id", ondelete="SET NULL"), nullable=True)

    #owner = relationship("ItemDatabaseUser")