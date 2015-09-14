# -*- coding: utf-8  -*-
"""
This module holds the database models for c3sMembership.

Tests for the code is in tests/test_models.py
and throughout the other bits of code.
"""

from datetime import (
    datetime,
)
from decimal import Decimal as D
import cryptacular.bcrypt

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Boolean,
    DateTime,
    Date,
    Unicode,
    or_,
    and_,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
# from sqlalchemy.sql.expression import func
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    synonym
)
import sqlalchemy.types as types

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def hash_password(password):
    return unicode(crypt.encode(password))


class SqliteNumeric(types.TypeDecorator):
    impl = types.String

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return D(value)

# can overwrite the imported type name
# @note: the TypeDecorator does not guarantie the scale and precision.
# you can do this with separate checks
Numeric = SqliteNumeric


class Group(Base):
    """
    The table of Groups.

    aka roles for users.

    Users in group 'staff' may do things others may not.
    """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Unicode(30), unique=True, nullable=False)

    def __str__(self):
        return 'group:%s' % self.name

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_staffers_group(cls, groupname=u'staff'):
        dbsession = DBSession()
        staff_group = dbsession.query(
            cls).filter(cls.name == groupname).first()
        return staff_group

#    @classmethod
#    def get_Users_group(cls, groupname="User"):
#        """Choose the right group for users"""
#        dbsession = DBSession()
#        users_group = dbsession.query(
#            cls).filter(cls.name == groupname).first()
#        print('=== get_Users_group:' + str(users_group))
#        return users_group


# table for relation between staffers and groups
staff_groups = Table(
    'staff_groups', Base.metadata,
    Column(
        'staff_id', Integer, ForeignKey('staff.id'),
        primary_key=True, nullable=False),
    Column(
        'group_id', Integer, ForeignKey('groups.id'),
        primary_key=True, nullable=False)
)


class C3sStaff(Base):
    """
    C3S staff may login and do things
    """
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    login = Column(Unicode(255), unique=True)
    '''- every user has a login name.'''
    _password = Column('password', Unicode(60))
    last_password_change = Column(
        DateTime,
        default=func.current_timestamp())
    email = Column(Unicode(255))
    groups = relationship(
        Group,
        secondary=staff_groups,
        backref="staff")

    def _init_(self, login, password, email):  # pragma: no cover
        self.login = login
        self.password = password
        self.last_password_change = datetime.now()
        self.email = email

    # @property
    # def __acl__(self):
    #    return [
    #        (Allow,                           # user may edit herself
    #         self.username, 'editUser'),
    #        #'user:%s' % self.username, 'editUser'),
    #        (Allow,                           # accountant group may edit
    #         'group:accountants', ('view', 'editUser')),
    #        (Allow,                           # admin group may edit
    #         'group:admins', ('view', 'editUser')),
    #    ]

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_login(cls, login):
        return DBSession.query(cls).filter(cls.login == login).first()

    @classmethod
    def check_password(cls, login, password):
        staffer = cls.get_by_login(login)
        return crypt.check(staffer.password, password)

    # this one is used by RequestWithUserAttribute
    @classmethod
    def check_user_or_None(cls, login):
        """
        check whether a user by that username exists in the database.
        if yes, return that object, else None.
        returns None if username doesn't exist
        """
        login = cls.get_by_login(login)  # is None if user not exists
        return login

    @classmethod
    def delete_by_id(cls, id):
        _del = DBSession.query(cls).filter(cls.id == id).first()
        _del.groups = []
        DBSession.query(cls).filter(cls.id == id).delete()
        return

    @classmethod
    def get_all(cls):
        """
        get all staff objects from the database
        """
        return DBSession.query(cls).all()


class Shares(Base):
    '''
    the database of shares

    once AFM submissions are complete, the part about the shares is moved here
    '''
    __tablename__ = 'shares'
    id = Column(Integer, primary_key=True)
    number = Column(Integer())  # how many
    date_of_acquisition = Column(DateTime(), nullable=False)  # when
    reference_code = Column(Unicode(255), unique=True)  # ex email_confirm_code
    signature_received = Column(Boolean, default=False)
    signature_received_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    signature_confirmed = Column(Boolean, default=False)
    signature_confirmed_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    payment_received = Column(Boolean, default=False)
    payment_received_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    payment_confirmed = Column(Boolean, default=False)
    payment_confirmed_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    accountant_comment = Column(Unicode(255))

    @classmethod
    def get_number(cls):
        """return number of entries (by counting rows in table)"""
        return DBSession.query(cls).count()

    @classmethod
    def get_max_id(cls):
        """return number of entries (by counting rows in table)"""
        res, = DBSession.query(func.max(cls.id)).first()
        # print("the result: {}".format(res,))
        return res

    @classmethod
    def get_by_id(cls, _id):
        """return one package of shares by id"""
        return DBSession.query(cls).filter(cls.id == _id).first()

    @classmethod
    def get_all(cls):
        """return all packages of shares"""
        return DBSession.query(cls).all()

    @classmethod
    def get_total_shares(cls):
        """return number of shares of accepted members"""
        all = DBSession.query(cls).all()
        total = 0
        for s in all:
            total += s.number
        return total

    @classmethod
    def delete_by_id(cls, _id):
        """delete one package of shares by id"""
        return DBSession.query(cls).filter(cls.id == _id).delete()

# table for relation between membership and shares
members_shares = Table(
    'members_shares', Base.metadata,
    Column(
        'members_id', Integer, ForeignKey('members.id'),
        primary_key=True, nullable=False),
    Column(
        'shares_id', Integer, ForeignKey('shares.id'),
        primary_key=True, nullable=False)
)


class C3sMember(Base):
    '''
    this table holds submissions to the C3S AFM form
    (AFM = application for membership)

    ..and has seen changes over time. additions:

    * crowdfunders,
    * founders from the initial assembly (RL!)
    * legal entities

    ..being turned into accepted members
    '''
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    # personal information
    firstname = Column(Unicode(255))
    lastname = Column(Unicode(255))
    email = Column(Unicode(255))
    _password = Column('password', Unicode(60))
    last_password_change = Column(
        DateTime,
        default=func.current_timestamp())
    # pass_reset_token = Column(Unicode(255))
    address1 = Column(Unicode(255))
    address2 = Column(Unicode(255))
    postcode = Column(Unicode(255))
    city = Column(Unicode(255))
    country = Column(Unicode(255))
    locale = Column(Unicode(255))
    date_of_birth = Column(Date(), nullable=False)
    email_is_confirmed = Column(Boolean, default=False)
    email_confirm_code = Column(Unicode(255), unique=True)  # reference code
    email_confirm_token = Column(Unicode(255), unique=True)  # token
    email_confirm_mail_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    # duplicate entries // people submitting at different times
    is_duplicate = Column(Boolean, default=False)
    is_duplicate_of = Column(Integer, nullable=True)
    # shares
    num_shares = Column(Integer())  # XXX TODO: check for number <= max_shares
    date_of_submission = Column(DateTime(), nullable=False)
    signature_received = Column(Boolean, default=False)
    signature_received_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    signature_confirmed = Column(Boolean, default=False)
    signature_confirmed_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    payment_received = Column(Boolean, default=False)
    payment_received_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    payment_confirmed = Column(Boolean, default=False)
    payment_confirmed_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    # shares in other table
    shares = relationship(
        Shares,
        secondary=members_shares,
        backref="members"
    )
    # reminders
    sent_signature_reminder = Column(Integer, default=0)
    sent_signature_reminder_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    sent_payment_reminder = Column(Integer, default=0)
    sent_payment_reminder_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    # comment
    accountant_comment = Column(Unicode(255))
    # membership information
    membership_type = Column(Unicode(255))
    member_of_colsoc = Column(Boolean, default=False)
    name_of_colsoc = Column(Unicode(255))
    # bureaucracy
    membership_accepted = Column(Boolean, default=False)
    membership_date = Column(
        DateTime(), default=datetime(1970, 1, 1))
    membership_number = Column(Integer())
    # startnex repair operations
    mtype_confirm_token = Column(Unicode(255))
    mtype_email_date = Column(DateTime(), default=datetime(1970, 1, 1))
    # invitations
    email_invite_flag_bcgv14 = Column(Boolean, default=False)
    email_invite_date_bcgv14 = Column(DateTime(), default=datetime(1970, 1, 1))
    email_invite_flag_bcgv15 = Column(Boolean, default=False)
    email_invite_date_bcgv15 = Column(DateTime(), default=datetime(1970, 1, 1))
    email_invite_token_bcgv15 = Column(Unicode(255))
    # legal entities
    is_legalentity = Column(Boolean, default=False)
    court_of_law = Column(Unicode(255))
    registration_number = Column(Unicode(255))
    # membership certificate
    certificate_email = Column(Boolean, default=False)
    certificate_token = Column(Unicode(10))
    certificate_email_date = Column(DateTime())
    # membership fees aka dues, for 2015
    dues15_invoice = Column(Boolean, default=False)  # sent?
    dues15_invoice_date = Column(DateTime())  # when?
    dues15_invoice_no = Column(Integer())  # lfd. nummer
    dues15_token = Column(Unicode(10))
    dues15_start = Column(Unicode(255))
    dues15_amount = Column(
        Numeric(12, 2), nullable=False, default=0)  # calculated
    dues15_paid = Column(Boolean, default=False)
    dues15_amount_paid = Column(
        Numeric(12, 2), nullable=False, default=0)
    dues15_paid_date = Column(DateTime())  # paid when?
    dues15_reduced = Column(Boolean, default=False)  # was reduced?
    dues15_amount_reduced = Column(
        Numeric(12, 2), nullable=False, default=0)  # ..to x
    
    def __init__(self, firstname, lastname, email, password,
                 address1, address2, postcode, city, country, locale,
                 date_of_birth, email_is_confirmed, email_confirm_code,
                 num_shares,
                 date_of_submission,
                 membership_type, member_of_colsoc, name_of_colsoc,
                 ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.last_password_change = datetime.now()
        self.address1 = address1
        self.address2 = address2
        self.postcode = postcode
        self.city = city
        self.country = country
        self.locale = locale
        self.date_of_birth = date_of_birth
        self.email_is_confirmed = email_is_confirmed
        self.email_confirm_code = email_confirm_code
        self.num_shares = num_shares
        self.date_of_submission = datetime.now()
        self.signature_received = False
        self.payment_received = False
        self.membership_type = membership_type
        self.member_of_colsoc = member_of_colsoc
        if self.member_of_colsoc is True:
            self.name_of_colsoc = name_of_colsoc
        else:
            self.name_of_colsoc = u''

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    @classmethod
    def get_by_code(cls, email_confirm_code):
        """
        find a member by confirmation code

        this is needed when a user returns from reading her email
        and clicking on a link containing the confirmation code.
        as the code is unique, one record is returned.
        """
        return DBSession.query(cls).filter(
            cls.email_confirm_code == email_confirm_code).first()

    # retired (not used any more)
    # @classmethod
    # def get_by_bcgvtoken(cls, token):
    #     """
    #     find a member by token used for GA and BarCamp

    #     this is needed when a user returns from reading her email
    #     and clicking on a link containing the token.
    #     .
    #     """
    #     return DBSession.query(cls).filter(
    #         cls.email_invite_token_bcgv15 == token).first()

    @classmethod
    def check_for_existing_confirm_code(cls, email_confirm_code):
        """
        check if a code is already present
        """
        check = DBSession.query(cls).filter(
            cls.email_confirm_code == email_confirm_code).first()
        if check:  # pragma: no cover
            return True
        else:
            return False

    @classmethod
    def get_by_id(cls, _id):
        """return one member by id"""
        return DBSession.query(cls).filter(cls.id == _id).first()

    @classmethod
    def get_by_email(cls, _email):
        """return one or more members by email (a list!)"""
        return DBSession.query(cls).filter(cls.email == _email).all()

    @classmethod
    def get_by_dues15_token(cls, _code):
        """return one member by fee token"""
        return DBSession.query(cls).filter(cls.dues15_token == _code).first()

    @classmethod
    def get_all(cls):
        """return all afms and members"""
        return DBSession.query(cls).all()

    # retired: not needed as of now
    # @classmethod
    # def get_invitees(cls, num):
    #    """return a given number of members to invite"""
    #    return DBSession.query(cls).filter(
    #        and_(
    #            cls.membership_accepted == 1,
    #            cls.email_invite_flag_bcgv15 == None
    #        )).slice(0, num).all()

    @classmethod
    def get_dues_invoicees(cls, num):
        """return a given number of members to send dues invoices to"""
        return DBSession.query(cls).filter(
            and_(
                cls.membership_accepted == 1,
                cls.dues15_invoice == 0
            )).slice(0, num).all()

    @classmethod
    def delete_by_id(cls, _id):
        """delete one member by id
        this will return 1 on success, 0 else
        """
        return DBSession.query(cls).filter(cls.id == _id).delete()

    # listings
    @classmethod
    def get_duplicates(cls):
        '''return the list of duplicates.'''
        return DBSession.query(cls).filter(
            cls.is_duplicate == 1).all()

    @classmethod
    def get_members(cls, order_by, how_many=10, offset=0, order="asc"):
        '''return the list accepted as members.'''
        try:
            attr = getattr(cls, order_by)
            order_function = getattr(attr, order)
        except:
            raise Exception("Invalid order_by ({0}) or order value "
                            "({1})".format(order_by, order))
        _how_many = int(offset) + int(how_many)
        _offset = int(offset)
        q = DBSession.query(cls).filter(
            cls.membership_accepted == 1
        ).order_by(order_function()).slice(_offset, _how_many)
        return q

    # statistical stuff
    @classmethod
    def get_postal_codes_de(cls):
        """return bag (list containing duplicates) of postal codes in DE"""
        all = DBSession.query(cls).filter(
            cls.country == 'DE'
        ).all()
        postal_codes_de = []
        for i in all:
            try:
                int(i.postcode)
                len(i.postcode) == 5
                postal_codes_de.append(i.postcode)
            except:
                print("exception at id {}: {}".format(
                    i.id,
                    i.postcode)
                )
                # pass
        return postal_codes_de

    # statistical stuff

    @classmethod
    def get_number(cls):
        """return number of submissions (by counting rows in table)"""
        return DBSession.query(cls).count()

    # @classmethod
    # def get_num_empty_slots(cls):
    #     """
    #     return number of submissions (by counting rows in table)
    #     awefully broken, needs fixing XXX
    #     """
    #     _all = DBSession.query(cls).all()
    #     print len(_all)
    #     _count = 0
    #     _found = []
    #     _range = [i for i in range(1, 1119)]
    #     max_id = 0
    #     print "_range: {}".format(_range)
    #     for i in _all:
    #         #print (i.id)
    #         assert(i.id is not None)
    #         if i.id > max_id:
    #             max_id = i.id
    #         _count += 1
    #         if i.id in _range:
    #             #print "removing {}".format(i.id)
    #             _range.remove(i.id)
    #             _found.extend([i.id])

    #     print "max_id: {}".format(max_id)
    #     print "loop finished. count is {}. len(_range) is {}. type: {}".format(
    #         _count, len(_range), type(_range))
    #     #print "_range: {}".format(_range)
    #     #print "_found: {}".format(_found)
    #     _diff = [x for x in _range if (x not in _found)]
    #     #print "_range - _found: {}".format(
    #         _diff)
    #     print "number of unused ids: {}".format(len(_diff))
    #     #from sqlalchemy import func
    #     #print "the max: {}".format(DBSession.query(func.max(cls.id)))
    #     return _count

    @classmethod
    def get_num_members_accepted(cls):
        '''
        count the members that have actually been accepted as members
        '''
        return DBSession.query(
            cls).filter(cls.membership_accepted == 1).count()

    @classmethod
    def get_num_non_accepted(cls):
        '''
        count the members that have actually been accepted as members
        '''
        return DBSession.query(
            cls).filter(or_(
                cls.membership_accepted != 1,
                cls.membership_accepted == 0,
                cls.membership_accepted == None,
            )).count()

    @classmethod
    def get_num_mem_nat_acc(cls):
        '''
        count the *persons* that have actually been accepted as members
        '''
        return DBSession.query(cls).filter(
            cls.is_legalentity == 0,
            cls.membership_accepted == 1,
        ).count()

    @classmethod
    def get_num_mem_jur_acc(cls):
        '''
        count the *legal entities* that have actually been accepted as members
        '''
        return DBSession.query(
            cls).filter(
                cls.is_legalentity == 1,
                cls.membership_accepted == 1
            ).count()

    @classmethod
    def get_num_mem_norm(cls):
        '''
        count the memberships that are normal members
        '''
        return DBSession.query(
            cls).filter(
                cls.membership_accepted == 1,
                cls.membership_type == 'normal'
            ).count()

    @classmethod
    def get_num_mem_invest(cls):
        '''
        count the memberships that are investing members
        '''
        return DBSession.query(
            cls).filter(
                cls.membership_accepted == 1,
                cls.membership_type == 'investing'
            ).count()

    @classmethod
    def get_num_mem_other_features(cls):
        '''
        count the memberships that are neither normal nor investing members
        '''
        _foo = DBSession.query(
            cls).filter(
                cls.membership_accepted == 1,
                cls.membership_type != 'normal',
                cls.membership_type != 'investing',
            ).all()
        # print "how many unknown: {}".format(len(_foo))
        _other = {}
        for i in _foo:
            if i.membership_type in _other.keys():
                _other[i.membership_type] += 1
            else:
                _other[i.membership_type] = 1
        # print "the options: {}".format(_other)
        return len(_foo)

    # listings
    @classmethod
    def member_listing(cls, order_by, how_many=10, offset=0, order="asc"):
        try:
            attr = getattr(cls, order_by)
            order_function = getattr(attr, order)
        except:
            raise Exception("Invalid order_by ({0}) or order value "
                            "({1})".format(order_by, order))
        _how_many = int(offset) + int(how_many)
        _offset = int(offset)
        q = DBSession.query(cls).order_by(order_function())\
                                .slice(_offset, _how_many)
        return q

    @classmethod
    def get_range_ids(cls, order_by, first_id, last_id, order="asc"):
        try:
            attr = getattr(cls, order_by)
            order_function = getattr(attr, order)
        except:
            raise Exception("Invalid order_by ({0}) or order value "
                            "({1})".format(order_by, order))
        q = DBSession.query(cls).filter(
            and_(
                cls.id >= first_id,
                cls.id <= last_id,
            )
        ).order_by(order_function()).all()
        return q

    @classmethod
    def nonmember_listing(cls, order_by, how_many, offset=0, order="asc"):
        try:
            attr = getattr(cls, order_by)
            order_function = getattr(attr, order)
        except:
            raise Exception("Invalid order_by ({0}) or order value "
                            "({1})".format(order_by, order))
        _how_many = int(offset) + int(how_many)
        _offset = int(offset)
        q = DBSession.query(cls).filter(
            or_(
                cls.membership_accepted == 0,
                cls.membership_accepted == '',
                cls.membership_accepted == None,
            )
        ).order_by(
            order_function()
        ).slice(_offset, _how_many)
        # print "length of nonmember listing: {}".format(q.count())
        # print "nonmember listing q: {}".format(q)
        return q.all()

    @classmethod
    def nonmember_listing_count(cls, order_by=u'id'):
        q = DBSession.query(cls).filter(
            or_(
                cls.membership_accepted == 0,
                cls.membership_accepted == '',
                cls.membership_accepted == None,
            )
        ).count()
        # print "length of nonmember listing: {}".format(q)
        # print "nonmember listing q: {}".format(q)
        return q

    @classmethod
    def get_num_nonmember_listing(cls):
        # cls.nonmember_listing(order_by='id').count()
        return cls.nonmember_listing_count()

    # count for statistics
    @classmethod
    def afm_num_shares_unpaid(cls):
        all = DBSession.query(cls).all()
        num_shares_unpaid = 0
        for item in all:
            if not item.payment_received:
                num_shares_unpaid += item.num_shares
        return num_shares_unpaid

    @classmethod
    def afm_num_shares_paid(cls):
        all = DBSession.query(cls).all()
        num_shares_paid = 0
        for item in all:
            if item.payment_received:
                num_shares_paid += item.num_shares
        return num_shares_paid

    # workflow: need approval by the board
    @classmethod
    def afms_ready_for_approval(cls):
        return DBSession.query(cls).filter(
            and_(
                (cls.membership_accepted == 0),
                (cls.signature_received),
                (cls.payment_received),
            )).all()

    # autocomplete
    @classmethod
    def get_matching_codes(cls, prefix):
        '''
        return only codes matchint the prefix
        '''
        all = DBSession.query(cls).all()
        codes = []
        for item in all:
            if item.email_confirm_code.startswith(prefix):
                codes.append(item.email_confirm_code)
        # print("number of items found: %s" % len(codes))
        return codes

    @classmethod
    def check_password(cls, _id, password):
        member = cls.get_by_id(_id)
        return crypt.check(member.password, password)

    # this one is used by RequestWithUserAttribute
    @classmethod
    def check_user_or_None(cls, _id):
        """
        check whether a user by that username exists in the database.
        if yes, return that object, else None.
        returns None if username doesn't exist
        """
        login = cls.get_by_id(_id)  # is None if user not exists
        return login

    # for merge comparisons
    @classmethod
    def get_same_lastnames(cls, name):  # XXX todo: similar
        """return list of accepted members with same lastnames"""
        return DBSession.query(cls).filter(
            and_(
                cls.membership_accepted == 1,
                cls.lastname == name
            )).all()

    @classmethod
    def get_same_firstnames(cls, name):  # XXX todo: similar
        """return list of accepted members with same fistnames"""
        return DBSession.query(cls).filter(
            and_(
                cls.membership_accepted == 1,
                cls.firstname == name
            )).all()

    @classmethod
    def get_same_email(cls, mail):  # XXX todo: similar
        """return list of accepted members with same email"""
        return DBSession.query(cls).filter(
            and_(
                cls.membership_accepted == 1,
                cls.email == mail,
            )).all()

    @classmethod
    def get_same_date_of_birth(cls, dob):  # XXX todo: similar
        """return list of accepted members with same date of birth"""
        return DBSession.query(cls).filter(
            and_(
                cls.membership_accepted == 1,
                cls.date_of_birth == dob,
            )).all()

    # membership numbers etc.
    @classmethod
    def get_num_membership_numbers(cls):
        '''
        count the number of membership numbers
        '''
        return DBSession.query(cls).filter(cls.membership_number).count()

    @classmethod
    def get_next_free_membership_number(cls):
        '''
        returns the next free membership number
        '''
        return C3sMember.get_highest_membership_number()+1

    @classmethod
    def get_highest_membership_number(cls):
        '''
        get the highest membership number
        '''
        nrs = DBSession.query(cls.membership_number).filter(
            cls.membership_number != None).all()
        _list = []
        for i in nrs:
            #print "-- {} -- {}".format(i, i[0])
            _list.append(int(i[0]))
        try:
            _max = max(_list)
        except:
            _list = [0, 999999999]
            _max = 999999999
        try:
            assert(_max == 999999999)
            _list.remove(max(_list))  # remove known maximum
        except:
            pass
        return max(_list)

    # countries
    @classmethod
    def get_num_countries(cls):
        '''return number of countries in DB'''
        _list = []
        _all = DBSession.query(cls)
        for item in _all:
            if item.country not in _list:
                _list.append(item.country)
        return len(_list)

    @classmethod
    def get_countries_list(cls):
        '''return dict of countries and number of occurrences'''
        _c_dict = {}
        _all = DBSession.query(cls)
        for item in _all:
            if item.country not in _c_dict.keys():
                # print u"adding {} to the list".format(item.country)
                _c_dict[item.country] = 1
            else:
                # print u"found one more entry for {}".format(item.country)
                _c_dict[item.country] += 1
        return _c_dict

    # autocomplete
    @classmethod
    def get_matching_people(cls, prefix):
        '''
        return only entries matchint the prefix
        '''
        all = DBSession.query(cls).all()
        names = {}
        for item in all:
            if item.lastname.startswith(prefix):
                _key = (
                    item.email_confirm_code + ' ' +
                    item.lastname + ', ' + item.firstname)
                names[_key] = _key
        return names


class Dues15Invoice(Base):
    """
    this table stores the invoices for the 2015 version of dues.
    we need this for bookkeeping,
    because whenever a member is granted a reduction of her dues,
    the old invoice is canceled by a reversal invoice
    and a new invoice must be issued.

    edge case: if reduced to 0, no new invoice needed.
    """
    __tablename__ = 'dues15invoices'
    id = Column(Integer, primary_key=True)
    # this invoice
    invoice_no = Column(Integer(), unique=True)
    invoice_no_string = Column(Unicode(255), unique=True)
    invoice_date = Column(DateTime())
    invoice_amount = Column(Numeric(12, 2), nullable=False, default=0)
    is_cancelled = Column(Boolean, default=False)
    is_reversal = Column(Boolean, default=False)
    cancelled_date = Column(DateTime())
    # person reference
    member_id = Column(Integer())
    membership_no = Column(Integer())
    email = Column(Unicode(255))
    token = Column(Unicode(255))
    # referrals
    preceding_invoice_no = Column(Integer(), default=None)
    succeeding_invoice_no = Column(Integer(), default=None)

    def __init__(self,
                 invoice_no,
                 invoice_no_string,
                 invoice_date,
                 invoice_amount,
                 member_id,
                 membership_no,
                 email,
                 token,
                 ):
        self.invoice_no = invoice_no
        self.invoice_no_string = invoice_no_string
        self.invoice_date = invoice_date
        self.invoice_amount = invoice_amount
        self.member_id = member_id
        self.membership_no = membership_no
        self.email = email
        self.token = token

    @classmethod
    def get_all(cls):
        """return all dues15 invoices"""
        return DBSession.query(cls).all()

    @classmethod
    def get_by_invoice_no(cls, _no):
        """return one invoice by invoice number"""
        return DBSession.query(cls).filter(cls.invoice_no == _no).first()

    @classmethod
    def get_by_membership_no(cls, _no):
        """return all invoices of one member by membership number"""
        return DBSession.query(cls).filter(cls.membership_no == _no).all()

    @classmethod
    def get_max_invoice_no(cls):
        """ return maximum of given invoice numbers or 0"""
        res, = DBSession.query(func.max(cls.id)).first()
        # print("the result: {}".format(res,))

        if res is None:
            return 0
        return res

    @classmethod
    def check_for_existing_dues15_token(cls, dues_token):
        """
        check if a dues token is already present
        """
        check = DBSession.query(cls).filter(
            cls.token == dues_token).first()
        if check:  # pragma: no cover
            return True
        else:
            return False

# # table for relation between membership and shares
# membership_shares = Table(
#     'membership_shares', Base.metadata,
#     Column(
#         'membership_id', Integer, ForeignKey('memberships.id'),
#         primary_key=True, nullable=False),
#     Column(
#         'shares_id', Integer, ForeignKey('shares.id'),
#         primary_key=True, nullable=False)
# )


# class Membership(Base):
#     '''
#     the database of memberships

#     single submissions of the form are to be merged here
#     '''
#     __tablename__ = 'memberships'
#     id = Column(Integer, primary_key=True)
#     # personal information
#     firstname = Column(Unicode(255))
#     lastname = Column(Unicode(255))
#     email = Column(Unicode(255))
#     _password = Column('password', Unicode(60))
#     last_password_change = Column(
#         DateTime,
#         default=func.current_timestamp())
#     address1 = Column(Unicode(255))
#     address2 = Column(Unicode(255))
#     postcode = Column(Unicode(255))
#     city = Column(Unicode(255))
#     country = Column(Unicode(255))
#     locale = Column(Unicode(255))
#     date_of_birth = Column(Date(), nullable=False)
#     email_is_confirmed = Column(Boolean, default=False)
#     email_confirmed_date = Column(
#         DateTime(), default=datetime(1970, 1, 1))
#     email_confirm_code = Column(Unicode(255), unique=True)
#     # shares
#     shares = relationship(
#         Shares,
#         secondary=membership_shares,
#         backref="memberships"
#     )
#     #num_shares = Column(Integer())
#         # XXX TODO: check for number <= max_shares
#     date_of_membership = Column(DateTime(), nullable=False)
#     accountant_comment = Column(Unicode(255))
#     # membership information
#     membership_type = Column(Unicode(255))
#     member_of_colsoc = Column(Boolean, default=False)
#     name_of_colsoc = Column(Unicode(255))

#     def __init__(self, firstname, lastname, email, password,
#                  address1, address2, postcode, city, country, locale,
#                  date_of_birth, email_is_confirmed,
#                  membership_type, member_of_colsoc, name_of_colsoc,
#                  date_of_membership=datetime.now(),
#                  ):
#         self.firstname = firstname
#         self.lastname = lastname
#         self.email = email
#         self.password = password
#         self.last_password_change = datetime.now()
#         self.address1 = address1
#         self.address2 = address2
#         self.postcode = postcode
#         self.city = city
#         self.country = country
#         self.locale = locale
#         self.date_of_birth = date_of_birth
#         self.email_is_confirmed = email_is_confirmed
#         self.date_of_membership = date_of_membership
#         self.membership_type = membership_type
#         self.member_of_colsoc = member_of_colsoc
#         if self.member_of_colsoc is True:
#             self.name_of_colsoc = name_of_colsoc
#         else:
#             self.name_of_colsoc = u''

#     def _get_password(self):
#         return self._password

#     def _set_password(self, password):
#         self._password = hash_password(password)

#     password = property(_get_password, _set_password)
#     password = synonym('_password', descriptor=password)

#     def get_num_shares(self):
#         num = 0
#         for s in self.shares:
#             num += s.number
#         return num

#     num_shares = property(get_num_shares)

#     @classmethod
#     def get_number(cls):
#         """return number of members (by counting rows in table)"""
#         return DBSession.query(cls).count()

#     @classmethod
#     def get_by_id(cls, _id):
#         """return one member by id"""
#         return DBSession.query(cls).filter(cls.id == _id).first()

#     # @classmethod
#     # def num_ms_nat(cls):
#     #     'number of memberships of natural persons'
#     #     return DBSession.query(cls).filter(
#     #         cls.membership_type == 'normal').first()

#     # @classmethod
#     # def num_ms_jur(cls):
#     #     'number of memberships of natural persons'
#     #     return DBSession.query(cls).filter(
#     #              cls.membership_type == 'normal').first()
#     @classmethod
#     def num_ms_norm(cls):
#         'number of memberships of natural persons'
#         return DBSession.query(cls).filter(
#             cls.membership_type == u'normal').count()

#     @classmethod
#     def num_ms_invest(cls):
#         'number of memberships of natural persons'
#         return DBSession.query(cls).filter(
#             cls.membership_type == u'investing').count()

#     @classmethod
#     def membership_listing(
#             cls, order_by, how_many=10, offset=0, order="asc"):
#         try:
#             attr = getattr(cls, order_by)
#             order_function = getattr(attr, order)
#         except:
#             raise Exception("Invalid order_by ({0}) or order value "
#                             "({1})".format(order_by, order))
#         _how_many = int(offset) + int(how_many)
#         _offset = int(offset)
#         q = DBSession.query(cls).order_by(order_function())\
#                                 .slice(_offset, _how_many)
#         return q

#     @classmethod
#     def get_same_lastnames(cls, name):  # XXX todo: similar
#         """return list of members with same lastnames"""
#         return DBSession.query(cls).filter(cls.lastname == name).slice(0, 10)

#     @classmethod
#     def get_same_email(cls, mail):  # XXX todo: similar
#         """return list of members with same email"""
#         return DBSession.query(cls).filter(cls.email == mail).slice(0, 10)
