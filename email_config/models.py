from django.db import models


class Address(models.Model):
    address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    added_by_user_id = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    partner_shipper_id = models.IntegerField(blank=True, null=True)
    address_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'


class AppCarrierModel(models.Model):
    trip_id = models.IntegerField(primary_key=True)
    vehicle_number = models.TextField()
    vehicle_type = models.TextField()
    company_name = models.TextField()
    lr_number = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    driver_name = models.TextField()
    consignor_name = models.TextField()
    consignee_name = models.TextField()
    trip_status = models.CharField(max_length=100)
    current_status = models.CharField(max_length=100)
    actual_unloading = models.CharField(max_length=100)
    total_distance = models.FloatField()
    dispatch_date = models.DateField()
    closure_date = models.DateField()
    closure_location = models.TextField()
    actuall_tt = models.FloatField()
    crossed_date = models.TextField()
    closure_type = models.TextField()
    actual_forward_tt = models.TextField()
    actual_reverse_tt = models.TextField()
    variance_tt = models.TextField()
    planned_forward_distance = models.TextField()
    planned_reverse_distance = models.TextField()
    actual_forward_distance = models.TextField()
    actual_reverse_distance = models.TextField()
    variance_distance = models.TextField()
    over_speed_instances = models.TextField()
    max_over_speed = models.TextField()
    safety_rating = models.TextField()
    planned_tt = models.TextField()

    class Meta:
        managed = False
        db_table = 'app_carrier_model'


class AppUser(models.Model):
    user_id = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    username = models.CharField(max_length=100)
    emailid = models.CharField(max_length=249, blank=True, null=True)
    password = models.CharField(max_length=50)
    user_status = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    role = models.ForeignKey('SuppRoles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_user'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Booking(models.Model):
    booking_id = models.TextField(unique=True, blank=True, null=True)
    booking_date = models.DateTimeField(blank=True, null=True)
    source = models.ForeignKey('Source', models.DO_NOTHING, blank=True, null=True)
    booking_status = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    final_drop = models.ForeignKey('Drops', models.DO_NOTHING, blank=True, null=True)
    booking_type = models.TextField(blank=True, null=True)
    payment_method = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    booking_way = models.TextField(blank=True, null=True)
    warehouse_name = models.TextField(blank=True, null=True)
    retry_booking = models.BooleanField(blank=True, null=True)
    customer_id = models.TextField(blank=True, null=True)
    drop_file_location = models.TextField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    warehouse_id = models.TextField(blank=True, null=True)
    logistic_booking_type = models.TextField(blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    user_email_id = models.TextField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    user_contact_number = models.TextField(blank=True, null=True)
    with_driver_application = models.BooleanField(blank=True, null=True)
    booking_device = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'booking'


class BookingCommercial(models.Model):
    trip_consignment = models.ForeignKey('TripConsignment', models.DO_NOTHING, blank=True, null=True)
    vehicle_type = models.TextField(blank=True, null=True)
    logistic_booking_type = models.TextField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    customer_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_tat = models.IntegerField(blank=True, null=True)
    customer_distance_km = models.FloatField(blank=True, null=True)
    carrier_company_id = models.IntegerField(blank=True, null=True)
    carrier_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_tat = models.IntegerField(blank=True, null=True)
    carrier_distance_km = models.FloatField(blank=True, null=True)
    vehicle_type_id = models.IntegerField(blank=True, null=True)
    carrier_company_name = models.TextField(blank=True, null=True)
    customer_company_name = models.TextField(blank=True, null=True)
    orig_address_id = models.IntegerField(blank=True, null=True)
    dest_address_id = models.IntegerField(blank=True, null=True)
    carrier_conversion_factor = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_pricing_type = models.TextField(blank=True, null=True)
    sku_code = models.TextField(blank=True, null=True)
    carton_code = models.TextField(blank=True, null=True)
    actual_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_volumetric_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_charged_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_basic_freight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_size = models.TextField(blank=True, null=True)
    carrier_uom_capacity_form = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_uom_capacity_to = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_price_per_kg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_fov = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_fov_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_fsc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_fsc_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_oda = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_docket_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_handing_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_loading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_unloading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_other_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_management_fee = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_management_fee_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_sub_total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_total_freight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_sgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_cgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_igst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_conversion_factor = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_pricing_type = models.TextField(blank=True, null=True)
    customer_basic_freight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_size = models.TextField(blank=True, null=True)
    customer_uom_capacity_form = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_uom_capacity_to = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_price_per_kg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_fov = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_fov_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_fsc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_fsc_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_oda = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_docket_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_handing_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_loading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_unloading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_other_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_management_fee = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_management_fee_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_sub_total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_total_freight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_sgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_cgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_igst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_oda_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_oda_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_volumetric_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_charged_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    volume_of_cargo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_contract_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    carrier_contract_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    carrier_rate_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    customer_rate_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    branch = models.ForeignKey('Branch', models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    source_state = models.TextField(blank=True, null=True)
    source_city = models.TextField(blank=True, null=True)
    source_location = models.TextField(blank=True, null=True)
    destination_state = models.TextField(blank=True, null=True)
    destination_city = models.TextField(blank=True, null=True)
    destination_location = models.TextField(blank=True, null=True)
    contracted_rate = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking_commercial'


class BookingOld(models.Model):
    booking_id = models.TextField(blank=True, null=True)
    consignor = models.ForeignKey('Consignor', models.DO_NOTHING)
    consignee = models.ForeignKey('Consignee', models.DO_NOTHING)
    booking_date = models.DateTimeField(blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    total_capacity = models.FloatField(blank=True, null=True)
    remaining_capacity = models.FloatField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    booking_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    time_stamp = models.DateTimeField(blank=True, null=True)
    payment_terms = models.TextField(blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    distance = models.TextField(blank=True, null=True)
    freight_status = models.TextField(blank=True, null=True)
    material_id = models.IntegerField(blank=True, null=True)
    partner_shipper_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking_old'


class Branch(models.Model):
    branch_name = models.TextField(blank=True, null=True)
    branch_address = models.TextField(blank=True, null=True)
    branch_lat = models.FloatField(blank=True, null=True)
    branch_lng = models.FloatField(blank=True, null=True)
    branch_code = models.IntegerField(blank=True, null=True)
    branch_gst = models.TextField(blank=True, null=True)
    branch_pan = models.TextField(blank=True, null=True)
    branch_cin = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'
        unique_together = (('branch_code', 'company_id'),)


class BranchUsers(models.Model):
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    branch_user_role = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch_users'


class CarrierCompany(models.Model):
    company_name = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    company_emailid = models.TextField(blank=True, null=True)
    logo = models.BinaryField(blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    businesstype = models.TextField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    phone_mobile = models.TextField(blank=True, null=True)
    branch = models.TextField(blank=True, null=True)
    master_company_id = models.IntegerField(blank=True, null=True)
    pancard = models.TextField(blank=True, null=True)
    gst = models.TextField(blank=True, null=True)
    status_updated_on = models.DateField(blank=True, null=True)
    verification_status = models.IntegerField(blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    account_holder_name = models.CharField(max_length=200, blank=True, null=True)
    bank_account_number = models.CharField(max_length=200, blank=True, null=True)
    bank_ifsc = models.CharField(max_length=200, blank=True, null=True)
    bank_branch = models.CharField(max_length=200, blank=True, null=True)
    company_cin_no = models.CharField(max_length=200, blank=True, null=True)
    franchisee_id = models.IntegerField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    auto_generate_carrier_company_code = models.TextField(blank=True, null=True)
    company_unique_code = models.CharField(max_length=200, blank=True, null=True)
    carrier_company_code = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrier_company'


class CarrierInvoice(models.Model):
    invoice_number = models.CharField(max_length=255)
    carrier_company_id = models.IntegerField()
    shipper_id = models.IntegerField(blank=True, null=True)
    shipment_id = models.CharField(max_length=100, blank=True, null=True)
    consignor = models.ForeignKey('Consignor', models.DO_NOTHING, blank=True, null=True)
    consignee = models.ForeignKey('Consignee', models.DO_NOTHING, blank=True, null=True)
    lr_no = models.CharField(max_length=-1, blank=True, null=True)
    pod_no = models.CharField(max_length=-1, blank=True, null=True)
    total_taxable_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_cgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_sgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_igst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_invoice_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    person_signature = models.TextField(blank=True, null=True)
    person_designation = models.TextField(blank=True, null=True)
    shipper_type = models.TextField(blank=True, null=True)
    place_of_supply = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    invoice_amount_in_word = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrier_invoice'


class CarrierZone(models.Model):
    zone = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    carrier_id = models.IntegerField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrier_zone'


class CityState(models.Model):
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city_state'
        unique_together = (('city', 'state', 'location'),)


class Cms(models.Model):
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms'


class CommercialContractType(models.Model):
    contract_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commercial_contract_type'


class Company(models.Model):
    company_name = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    company_emailid = models.TextField(blank=True, null=True)
    logo = models.BinaryField(blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    businesstype = models.TextField(blank=True, null=True)  # This field type is a guess.
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    time_stamp = models.DateTimeField(blank=True, null=True)
    phone_mobile = models.TextField(blank=True, null=True)
    branch = models.TextField(blank=True, null=True)
    master_company_id = models.IntegerField(blank=True, null=True)
    pancard = models.TextField(blank=True, null=True)
    gst = models.TextField(blank=True, null=True)
    status_updated_on = models.DateField(blank=True, null=True)
    verification_status = models.IntegerField(blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    account_holder_name = models.CharField(max_length=200, blank=True, null=True)
    bank_account_number = models.CharField(max_length=200, blank=True, null=True)
    bank_ifsc = models.CharField(max_length=200, blank=True, null=True)
    bank_branch = models.CharField(max_length=200, blank=True, null=True)
    company_cin_no = models.CharField(max_length=200, blank=True, null=True)
    company_unique_code = models.CharField(max_length=200, blank=True, null=True)
    franchisee_id = models.IntegerField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    carrier_company_code = models.TextField(blank=True, null=True)
    auto_generate_carrier_company_code = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class CompanyGpsProvider(models.Model):
    gps_provider = models.IntegerField()
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    company_id = models.IntegerField()
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_gps_provider'


class CompanyTransaction(models.Model):
    company_transaction_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    transo_credits = models.IntegerField(blank=True, null=True)
    transo_money = models.IntegerField(blank=True, null=True)
    updated_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_transaction'


class CompanyType(models.Model):
    type = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_type'


class Companydocumentlist(models.Model):
    id = models.AutoField()
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companydocumentlist'


class Companydocuments(models.Model):
    document = models.BinaryField(blank=True, null=True)
    verified = models.TextField(blank=True, null=True)  # This field type is a guess.
    verification_reason = models.TextField(blank=True, null=True)
    documentid = models.IntegerField(blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companydocuments'


class Companydocumentsbackup(models.Model):
    id = models.IntegerField(blank=True, null=True)
    document = models.BinaryField(blank=True, null=True)
    verified = models.TextField(blank=True, null=True)  # This field type is a guess.
    verification_reason = models.TextField(blank=True, null=True)
    documentid = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companydocumentsbackup'


class Consignee(models.Model):
    company_name = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    mobile = models.TextField(blank=True, null=True)
    landline = models.TextField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    added_by = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consignee'


class ConsignmentInvoices(models.Model):
    invoice_no = models.TextField(blank=True, null=True)
    invoice_value = models.IntegerField(blank=True, null=True)
    invoice_image = models.BinaryField(blank=True, null=True)
    shipment_details = models.ForeignKey('ShipmentDetails', models.DO_NOTHING, blank=True, null=True)
    consignment_id = models.TextField(blank=True, null=True)
    drop_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consignment_invoices'


class Consignor(models.Model):
    company_name = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    mobile = models.TextField(blank=True, null=True)
    landline = models.TextField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    added_by = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consignor'


class Contacts(models.Model):
    company_name = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    mobile = models.TextField(blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts'


class ContractTypes(models.Model):
    contract_type_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_types'


class Customer(models.Model):
    customer_company = models.TextField(blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    customer_email_id = models.TextField(blank=True, null=True)
    customer_company_cin = models.CharField(max_length=-1, blank=True, null=True)
    customer_company_pan = models.CharField(max_length=255, blank=True, null=True)
    customer_company_gst = models.CharField(max_length=255, blank=True, null=True)
    customer_phone_no = models.TextField(blank=True, null=True)
    auto_customer_code = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    customer_code = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    gst_percentage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_code_created_date = models.DateTimeField(blank=True, null=True)
    product_category = models.TextField(blank=True, null=True)
    soft_delete = models.BooleanField(blank=True, null=True)
    product_category_0 = models.ForeignKey('MaterialType', models.DO_NOTHING, db_column='product_category_id', blank=True, null=True)  # Field renamed because of name conflict.
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'
        unique_together = (('customer_code', 'company_id'),)


class CustomerContractRouteRate(models.Model):
    customer_id = models.IntegerField(blank=True, null=True)
    source_state = models.TextField(blank=True, null=True)
    destination_state = models.TextField(blank=True, null=True)
    source_city = models.TextField(blank=True, null=True)
    destination_city = models.TextField(blank=True, null=True)
    rate = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_contract_route_rate'


class CustomerLrFormat(models.Model):
    lr_format = models.TextField(unique=True, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    pod_format = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, unique=True, blank=True, null=True)
    no_of_lr = models.IntegerField(blank=True, null=True)
    requested_lr_stock = models.IntegerField(blank=True, null=True)
    no_of_stationary_manual_lr = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_lr_format'


class CustomerLrNumbers(models.Model):
    customer_lr_number = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    used_by_branch_id = models.TextField(blank=True, null=True)
    added_datetime = models.DateTimeField(blank=True, null=True)
    used_datetime = models.DateTimeField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    branch_code = models.IntegerField(blank=True, null=True)
    branch_name = models.TextField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    lr_type = models.TextField(blank=True, null=True)
    branch_code_sequence = models.IntegerField(blank=True, null=True)
    final_status = models.TextField(blank=True, null=True)
    final_status_datetime = models.DateTimeField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    added_on_time_stamp = models.DateTimeField(blank=True, null=True)
    warehouse_required_lr_stock = models.IntegerField(blank=True, null=True)
    warehouse_lr_allocation_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    stationary_lr = models.BooleanField(blank=True, null=True)
    transferred_from_warehouse_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_lr_numbers'


class CustomerZone(models.Model):
    zone = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_zone'


class Customeraddress(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    address_name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    contact_number = models.TextField(blank=True, null=True)
    contact_email = models.TextField(blank=True, null=True)
    contact_code = models.TextField(unique=True, blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    google_map_address = models.TextField(blank=True, null=True)
    address_line_one = models.TextField(blank=True, null=True)
    address_line_two = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    contact_code_created_date = models.DateTimeField(blank=True, null=True)
    pan_number = models.TextField(blank=True, null=True)
    soft_delete = models.BooleanField(blank=True, null=True)
    product_category = models.TextField(blank=True, null=True)
    product_category_material_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customeraddress'


class DailyVehicleKm(models.Model):
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING)
    date = models.DateField(blank=True, null=True)
    km = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    update_on = models.DateTimeField(blank=True, null=True)
    driving_time = models.FloatField(blank=True, null=True)
    avg_speed = models.FloatField(blank=True, null=True)
    stoppage_time = models.FloatField(blank=True, null=True)
    error = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_vehicle_km'


class DetailedViolations(models.Model):
    id = models.BigAutoField()
    imei = models.TextField()
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    event_type = models.TextField(blank=True, null=True)
    email_sent = models.BooleanField()
    event_value = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    location_points = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detailed_violations'
        unique_together = (('imei', 'start_time', 'event_type'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Documenttype(models.Model):
    document_desc = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documenttype'


class Driver(models.Model):
    password = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    authorisation_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    timestamp = models.DateTimeField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    profilepic = models.BinaryField(blank=True, null=True)
    phone_mobile = models.TextField(blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    emailid = models.TextField(blank=True, null=True)
    company_id = models.AutoField()
    vehicleid = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='vehicleid', blank=True, null=True)
    dob = models.TextField(blank=True, null=True)
    verification_status = models.IntegerField(blank=True, null=True)
    app_version = models.TextField(blank=True, null=True)
    device_name = models.TextField(blank=True, null=True)
    dl_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver'
        unique_together = (('emailid', 'phone_mobile'),)


class DriverDocumentVerification(models.Model):
    document_type = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    job_id = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    file_location = models.TextField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver_document_verification'


class DriverEvents(models.Model):
    driver = models.ForeignKey(Driver, models.DO_NOTHING, blank=True, null=True)
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, blank=True, null=True)
    trip_id = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey('Events', models.DO_NOTHING, blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver_events'


class DriverKyc(models.Model):
    kyc_id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, models.DO_NOTHING, blank=True, null=True)
    job_id = models.TextField(blank=True, null=True)
    document_link = models.TextField(blank=True, null=True)
    kyc_status = models.TextField(blank=True, null=True)
    kyc_failure_reason = models.TextField(blank=True, null=True)
    vehicle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver_kyc'


class DriverTemp(models.Model):
    id = models.BigAutoField(primary_key=True)
    firstname = models.TextField(blank=True, null=True)
    phone_mobile = models.TextField(blank=True, null=True)
    regno = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver_temp'


class Driverdocumentlist(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driverdocumentlist'


class Driverdocuments(models.Model):
    document = models.BinaryField(blank=True, null=True)
    verified = models.TextField(blank=True, null=True)  # This field type is a guess.
    verification_reason = models.TextField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    documentid = models.ForeignKey(Driverdocumentlist, models.DO_NOTHING, db_column='documentid', blank=True, null=True)
    driver = models.ForeignKey(Driver, models.DO_NOTHING, blank=True, null=True)
    updated_status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driverdocuments'


class DropTripEvents(models.Model):
    trip = models.ForeignKey('Trip', models.DO_NOTHING, blank=True, null=True)
    drop = models.ForeignKey('Drops', models.DO_NOTHING, blank=True, null=True)
    event = models.ForeignKey('Events', models.DO_NOTHING, blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drop_trip_events'


class Drops(models.Model):
    company_name = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    mobile = models.TextField(blank=True, null=True)
    landline = models.TextField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    added_by = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    customeraddress_id = models.IntegerField(blank=True, null=True)
    address_name = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drops'


class EmailReports(models.Model):
    email_reports_id = models.BigAutoField(primary_key=True)
    reports = models.ForeignKey('Reports', models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_reports'


class Events(models.Model):
    event_name = models.TextField(blank=True, null=True)
    event_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class ExpenseEvents(models.Model):
    event_name = models.TextField(blank=True, null=True)
    event_desc = models.TextField(blank=True, null=True)
    quantity = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expense_events'


class Expenses(models.Model):
    trip_id = models.IntegerField(blank=True, null=True)
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING)
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    expens_event = models.ForeignKey(ExpenseEvents, models.DO_NOTHING)
    quantity = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    odometer_reading = models.IntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expenses'


class ExpensesOld(models.Model):
    trip_id = models.IntegerField(blank=True, null=True)
    vehicle_id = models.IntegerField()
    driver_id = models.IntegerField()
    expens_event_id = models.IntegerField()
    quantity = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expenses_old'


class FtlCarrMaster(models.Model):
    id = models.AutoField()
    carrier_id = models.IntegerField(blank=True, null=True)
    vehicle_type_id = models.IntegerField(blank=True, null=True)
    orig_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    dest_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    agreed_price = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    row_status = models.CharField(max_length=1, blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)
    pending_data = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    contract_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    rate_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_state = models.TextField(blank=True, null=True)
    from_city = models.TextField(blank=True, null=True)
    from_taluk = models.TextField(blank=True, null=True)
    from_location = models.TextField(blank=True, null=True)
    to_state = models.TextField(blank=True, null=True)
    to_city = models.TextField(blank=True, null=True)
    to_taluk = models.TextField(blank=True, null=True)
    to_location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftl_carr_master'
        unique_together = (('carrier_id', 'branch', 'warehouse', 'vehicle_type_id', 'from_state', 'from_city', 'from_location', 'to_state', 'to_city', 'to_location', 'rate_type'),)


class FtlCustMaster(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    vehicle_type_id = models.IntegerField(blank=True, null=True)
    orig_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    dest_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    agreed_price = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    row_status = models.CharField(max_length=1, blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)
    pending_data = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    contract_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    rate_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_state = models.TextField(blank=True, null=True)
    from_city = models.TextField(blank=True, null=True)
    from_taluk = models.TextField(blank=True, null=True)
    from_location = models.TextField(blank=True, null=True)
    to_state = models.TextField(blank=True, null=True)
    to_city = models.TextField(blank=True, null=True)
    to_taluk = models.TextField(blank=True, null=True)
    to_location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftl_cust_master'
        unique_together = (('customer', 'branch', 'warehouse', 'vehicle_type_id', 'from_state', 'from_city', 'from_location', 'to_state', 'to_city', 'to_location', 'rate_type'),)


class FtlShipmentTracking(models.Model):
    pickup_schedule_date = models.DateTimeField(blank=True, null=True)
    vehicle_placed_date_time_at_origin = models.DateTimeField(blank=True, null=True)
    vehicle_reported_date_time_at_destination = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    vendor_bills_ageing = models.TextField(blank=True, null=True)
    present_status = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    vehicle_released_date_time_at_destination = models.DateTimeField(blank=True, null=True)
    pod_status = models.TextField(blank=True, null=True)
    pod_submit = models.TextField(blank=True, null=True)
    pod_submission_date = models.DateTimeField(blank=True, null=True)
    total_km = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    avarage_km_covered_day = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tgt_km_covered = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    actual_days = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    actual_km = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    balance_km = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ontime_delay = models.TextField(blank=True, null=True)
    ontime_delay_percentage = models.TextField(blank=True, null=True)
    actual_days_of_delivery = models.TextField(blank=True, null=True)
    delayed_reason = models.TextField(blank=True, null=True)
    halting_days = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    day = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    drop_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftl_shipment_tracking'


class GeofenceLocation(models.Model):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geofence_location'


class GpsDeviceProvider(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gps_device_provider'


class GstRate(models.Model):
    sgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    igst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tds = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gst_rate'


class Indianoil(models.Model):
    merchant_id = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    dealer_sap_code = models.TextField(blank=True, null=True)
    retailoutletname = models.TextField(blank=True, null=True)
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    address3 = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    contact_mobile = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    dealer_code = models.TextField(blank=True, null=True)
    transport_hub = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indianoil'


class Invoice(models.Model):
    billno = models.TextField(blank=True, null=True)
    shipmentid = models.TextField(blank=True, null=True)
    carrierid = models.TextField(blank=True, null=True)
    carriername = models.TextField(blank=True, null=True)
    shipperid = models.TextField(blank=True, null=True)
    shippername = models.TextField(blank=True, null=True)
    gstno = models.TextField(blank=True, null=True)
    shipmentdate = models.TextField(blank=True, null=True)
    consignorname = models.TextField(blank=True, null=True)
    consignorphone = models.TextField(blank=True, null=True)
    consignoraddr = models.TextField(blank=True, null=True)
    consigneename = models.TextField(blank=True, null=True)
    consigneephone = models.TextField(blank=True, null=True)
    consigneeaddr = models.TextField(blank=True, null=True)
    lrno = models.TextField(blank=True, null=True)
    podno = models.TextField(blank=True, null=True)
    shipmentweight = models.TextField(blank=True, null=True)
    freight = models.TextField(blank=True, null=True)
    paymentstatus = models.TextField(blank=True, null=True)
    invoicestatus = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    drop_id = models.IntegerField(blank=True, null=True)
    consignment_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceParticular(models.Model):
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING)
    particular = models.CharField(max_length=255, blank=True, null=True)
    shipment_quantity = models.TextField(blank=True, null=True)
    final_weight = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    taxable_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cgst_rate = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cgst_amount = models.TextField(blank=True, null=True)
    sgst_rate = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sgst_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    igst_rate = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    igst_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hsn_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_particular'


class JrmRoutes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jrm_routes'


class Logisticscompany(models.Model):
    company_name = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    company_emailid = models.TextField(blank=True, null=True)
    logo = models.BinaryField(blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    businesstype = models.TextField(blank=True, null=True)  # This field type is a guess.
    role_id = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    phone_mobile = models.TextField(blank=True, null=True)
    pancard = models.TextField(blank=True, null=True)
    gst = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logisticscompany'


class LrBranchCode(models.Model):
    branch_name_location = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    branch_code = models.IntegerField(blank=True, null=True)
    gst_in = models.TextField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lr_branch_code'


class LrReceipt(models.Model):
    lr_number = models.CharField(max_length=254)
    customer_name = models.CharField(max_length=254)
    origin = models.CharField(max_length=254)
    destination = models.CharField(max_length=254)
    booking_date = models.CharField(max_length=254)
    number_of_boxes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lr_receipt'


class LtlCarrMaster(models.Model):
    carrier_id = models.IntegerField(blank=True, null=True)
    orig_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    dest_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    row_status = models.TextField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    contract_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    rate_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_state = models.TextField(blank=True, null=True)
    from_city = models.TextField(blank=True, null=True)
    from_location = models.TextField(blank=True, null=True)
    to_state = models.TextField(blank=True, null=True)
    to_city = models.TextField(blank=True, null=True)
    to_location = models.TextField(blank=True, null=True)
    from_zone = models.TextField(blank=True, null=True)
    to_zone = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    temp_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltl_carr_master'
        unique_together = (('carrier_id', 'branch_id', 'warehouse_id', 'from_state', 'from_city', 'from_location', 'to_state', 'to_city', 'to_location', 'from_zone', 'to_zone', 'rate_type'),)


class LtlCarrMasterTemp(models.Model):
    carrier = models.ForeignKey(CarrierCompany, models.DO_NOTHING, blank=True, null=True)
    orig_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    dest_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    row_status = models.TextField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    contract_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    rate_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_state = models.TextField(blank=True, null=True)
    from_city = models.TextField(blank=True, null=True)
    from_location = models.TextField(blank=True, null=True)
    to_state = models.TextField(blank=True, null=True)
    to_city = models.TextField(blank=True, null=True)
    to_location = models.TextField(blank=True, null=True)
    from_zone = models.TextField(blank=True, null=True)
    to_zone = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    branch = models.TextField(blank=True, null=True)
    warehouse = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    ltl_carr_master_id = models.IntegerField(blank=True, null=True)
    conv_factor = models.IntegerField(blank=True, null=True)
    pricing_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    size = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_cap = models.IntegerField(blank=True, null=True)
    to_cap = models.IntegerField(blank=True, null=True)
    price_per_kg = models.FloatField(blank=True, null=True)
    fov = models.FloatField(blank=True, null=True)
    fsc = models.FloatField(blank=True, null=True)
    oda = models.FloatField(blank=True, null=True)
    docket_chrgs = models.FloatField(blank=True, null=True)
    handling_chrgs = models.FloatField(blank=True, null=True)
    mgmt_fee = models.FloatField(blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ltl_carr_master_temp'
        unique_together = (('carrier', 'branch_id', 'warehouse_id', 'from_state', 'from_city', 'from_location', 'to_state', 'to_city', 'to_location', 'from_zone', 'to_zone', 'rate_type'),)


class LtlCarrSlab(models.Model):
    ltl_carr_master = models.ForeignKey(LtlCarrMaster, models.DO_NOTHING, blank=True, null=True)
    conv_factor = models.IntegerField(blank=True, null=True)
    pricing_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    size = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_cap = models.IntegerField(blank=True, null=True)
    to_cap = models.IntegerField(blank=True, null=True)
    price_per_kg = models.FloatField(blank=True, null=True)
    fov = models.FloatField(blank=True, null=True)
    fsc = models.FloatField(blank=True, null=True)
    oda = models.FloatField(blank=True, null=True)
    docket_chrgs = models.FloatField(blank=True, null=True)
    handling_chrgs = models.FloatField(blank=True, null=True)
    mgmt_fee = models.FloatField(blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    pending_data = models.TextField(blank=True, null=True)
    ltl_cust_slab_master_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltl_carr_slab'


class LtlCarrSlabTemp(models.Model):
    ltl_carr_master = models.ForeignKey(LtlCarrMasterTemp, models.DO_NOTHING, blank=True, null=True)
    conv_factor = models.IntegerField(blank=True, null=True)
    pricing_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    size = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_cap = models.IntegerField(blank=True, null=True)
    to_cap = models.IntegerField(blank=True, null=True)
    price_per_kg = models.FloatField(blank=True, null=True)
    fov = models.FloatField(blank=True, null=True)
    fsc = models.FloatField(blank=True, null=True)
    oda = models.FloatField(blank=True, null=True)
    docket_chrgs = models.FloatField(blank=True, null=True)
    handling_chrgs = models.FloatField(blank=True, null=True)
    mgmt_fee = models.FloatField(blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    pending_data = models.TextField(blank=True, null=True)
    ltl_cust_slab_master_temp_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltl_carr_slab_temp'


class LtlCustMaster(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    orig_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    dest_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    contract_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    rate_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_state = models.TextField(blank=True, null=True)
    from_city = models.TextField(blank=True, null=True)
    from_location = models.TextField(blank=True, null=True)
    to_state = models.TextField(blank=True, null=True)
    to_city = models.TextField(blank=True, null=True)
    to_location = models.TextField(blank=True, null=True)
    from_zone = models.TextField(blank=True, null=True)
    to_zone = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ltl_cust_master'
        unique_together = (('customer', 'branch_id', 'warehouse_id', 'from_state', 'from_city', 'from_location', 'to_state', 'to_city', 'to_location', 'from_zone', 'to_zone', 'rate_type'),)


class LtlCustSlab(models.Model):
    ltl_cust_master = models.ForeignKey(LtlCustMaster, models.DO_NOTHING, blank=True, null=True)
    conv_factor = models.IntegerField(blank=True, null=True)
    pricing_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    size = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_cap = models.IntegerField(blank=True, null=True)
    to_cap = models.IntegerField(blank=True, null=True)
    price_per_kg = models.FloatField(blank=True, null=True)
    fov = models.FloatField(blank=True, null=True)
    fsc = models.FloatField(blank=True, null=True)
    oda = models.FloatField(blank=True, null=True)
    docket_chrgs = models.FloatField(blank=True, null=True)
    handling_chrgs = models.FloatField(blank=True, null=True)
    mgmt_fee = models.FloatField(blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    pending_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltl_cust_slab'


class LtlPendingBooking(models.Model):
    destination_address = models.TextField(blank=True, null=True)
    destination_lattitude = models.FloatField(blank=True, null=True)
    destination_longitude = models.FloatField(blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    consignee_mobile_no = models.TextField(blank=True, null=True)
    consignee_email_id = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    vendor_lr_number = models.TextField(blank=True, null=True)
    lr_number = models.CharField(max_length=-1, blank=True, null=True)
    ewaybill_number = models.TextField(blank=True, null=True)
    ewaybill_valid_from_date = models.DateTimeField(blank=True, null=True)
    ewaybill_valid_to_date = models.DateTimeField(blank=True, null=True)
    invoice_number = models.TextField(blank=True, null=True)
    invoice_date = models.DateTimeField(blank=True, null=True)
    vendor_lr_date = models.DateTimeField(blank=True, null=True)
    length = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    breadth = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    actual_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    volumetric_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_loading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_unloading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_other_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sku_code = models.TextField(blank=True, null=True)
    carton_code = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    material_type = models.TextField(blank=True, null=True)
    material_type_0 = models.ForeignKey('MaterialType', models.DO_NOTHING, db_column='material_type_id', blank=True, null=True)  # Field renamed because of name conflict.
    destination_address_name = models.TextField(blank=True, null=True)
    destination_address_id = models.IntegerField(blank=True, null=True)
    origin_address_id = models.IntegerField(blank=True, null=True)
    origin_address_name = models.TextField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    carrier_company_name = models.TextField(blank=True, null=True)
    carrier_company_id = models.IntegerField(blank=True, null=True)
    vendor_loading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    vendor_unloading_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    vendor_other_charge = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    surcharges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cover_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cover_collection_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    door_collection_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    door_delivery_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    value_added_services = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    statistical_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    misc_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    invoice_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    no_of_box = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltl_pending_booking'


class LtlShipmentTracking(models.Model):
    drop_id = models.IntegerField(blank=True, null=True)
    scanned_location = models.TextField(blank=True, null=True)
    event_description = models.TextField(blank=True, null=True)
    scan_time = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    scan_date = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    master_trip_id = models.IntegerField(blank=True, null=True)
    trip_id = models.IntegerField(blank=True, null=True)
    trip_consignment_id = models.IntegerField(blank=True, null=True)
    vendor_lr_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltl_shipment_tracking'


class LtlUomRange(models.Model):
    id = models.AutoField()
    range = models.TextField(blank=True, null=True)
    slab = models.TextField(blank=True, null=True)
    fixed = models.TextField(blank=True, null=True)
    lumpsum = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltl_uom_range'


class ManufactureType(models.Model):
    id = models.AutoField()
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manufacture_type'


class MasterCompany(models.Model):
    id = models.AutoField()
    company_name = models.TextField(db_column='Company_name')  # Field name made lowercase.
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_company'


class MasterTrip(models.Model):
    master_trip_id = models.TextField()
    status = models.TextField(blank=True, null=True)
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING)
    not_accepted_status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_trip'


class MaterialType(models.Model):
    material = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_type'


class Notifications(models.Model):
    id = models.AutoField()
    sender = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    sender_displayname = models.TextField(blank=True, null=True)
    notification_scope = models.TextField(blank=True, null=True)  # This field type is a guess.
    notification_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    notification_msg = models.TextField(blank=True, null=True)
    receiver_userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='receiver_userid', blank=True, null=True)
    receiver_role = models.ForeignKey('Roles', models.DO_NOTHING, db_column='receiver_role', blank=True, null=True)
    action_required = models.BooleanField(blank=True, null=True)
    action_type = models.TextField(blank=True, null=True)
    action_link = models.TextField(blank=True, null=True)
    notification_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    notification_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class OtpData(models.Model):
    phone_mobile = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    otp = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otp_data'


class Particulars(models.Model):
    id = models.IntegerField(primary_key=True)
    particular = models.TextField(blank=True, null=True)
    hsn_code = models.CharField(max_length=20, blank=True, null=True)
    cgst_rate = models.IntegerField(blank=True, null=True)
    sgst_rate = models.IntegerField(blank=True, null=True)
    igst_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'particulars'


class PartnerShipper(models.Model):
    carrier_company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    person_name = models.TextField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)
    company_cin = models.CharField(max_length=255, blank=True, null=True)
    company_pan = models.CharField(max_length=255, blank=True, null=True)
    company_gst = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.TextField(blank=True, null=True)
    shipper_company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_shipper'


class PendingBookingConsignmentPackageDetails(models.Model):
    pending_booking = models.ForeignKey(LtlPendingBooking, models.DO_NOTHING, blank=True, null=True)
    no_of_box = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    breadth = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pending_booking_consignment_package_details'


class PermitTypes(models.Model):
    permit_type_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permit_types'


class Pincode(models.Model):
    pincode_id = models.AutoField(primary_key=True)
    pincode = models.TextField(blank=True, null=True)
    area_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pincode'


class RcDocumentVerification(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehicle_number = models.TextField(blank=True, null=True)
    body_type = models.TextField(blank=True, null=True)
    cubic_capacity = models.TextField(blank=True, null=True)
    financed = models.TextField(blank=True, null=True)
    financer = models.TextField(blank=True, null=True)
    fuel_type = models.TextField(blank=True, null=True)
    insurance_company = models.TextField(blank=True, null=True)
    manufacturing_date = models.TextField(blank=True, null=True)
    national_permit_issued_by = models.TextField(blank=True, null=True)
    national_permit_number = models.TextField(blank=True, null=True)
    national_permit_upto = models.TextField(blank=True, null=True)
    permit_issue_date = models.TextField(blank=True, null=True)
    permit_type = models.TextField(blank=True, null=True)
    permit_valid_from = models.TextField(blank=True, null=True)
    permit_valid_upto = models.TextField(blank=True, null=True)
    rc_number = models.TextField(blank=True, null=True)
    rc_status = models.TextField(blank=True, null=True)
    registration_date = models.TextField(blank=True, null=True)
    seat_capacity = models.TextField(blank=True, null=True)
    vehicle_category = models.TextField(blank=True, null=True)
    vehicle_chasi_number = models.TextField(blank=True, null=True)
    vehicle_engine_number = models.TextField(blank=True, null=True)
    vehicle_gross_weight = models.TextField(blank=True, null=True)
    rc_verification_status = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    driver_id = models.TextField(blank=True, null=True)
    vehicle_id = models.TextField(blank=True, null=True)
    company_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rc_document_verification'


class Reports(models.Model):
    reports_id = models.BigAutoField(primary_key=True)
    reports_name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports'


class Roles(models.Model):
    rolename = models.TextField(blank=True, null=True)
    roleenabled = models.BooleanField(blank=True, null=True)
    roledesc = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    company_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class RolesBak16Sep2020(models.Model):
    id = models.IntegerField(blank=True, null=True)
    rolename = models.TextField(blank=True, null=True)
    roleenabled = models.BooleanField(blank=True, null=True)
    roledesc = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_bak_16sep2020'


class RoundTrip(models.Model):
    round_trip_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    vehicle_id = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round_trip'


class RoundTripCarrMaster(models.Model):
    carrier = models.ForeignKey(CarrierCompany, models.DO_NOTHING, blank=True, null=True)
    vehicle_type_id = models.IntegerField(blank=True, null=True)
    orig_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    dest_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    agreed_price = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)
    pending_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round_trip_carr_master'
        unique_together = (('carrier', 'vehicle_type_id', 'orig_address', 'dest_address'),)


class RoundTripCustMaster(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    vehicle_type_id = models.IntegerField(blank=True, null=True)
    orig_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    dest_address = models.ForeignKey(Customeraddress, models.DO_NOTHING, blank=True, null=True)
    distance_km = models.FloatField(blank=True, null=True)
    agreed_price = models.FloatField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    pending_data = models.TextField(blank=True, null=True)
    approval_status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round_trip_cust_master'
        unique_together = (('customer', 'vehicle_type_id', 'orig_address', 'dest_address'),)


class Route(models.Model):
    source = models.ForeignKey(GeofenceLocation, models.DO_NOTHING, blank=True, null=True)
    destination = models.ForeignKey(GeofenceLocation, models.DO_NOTHING, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    radius = models.TextField(blank=True, null=True)
    source_address = models.TextField(blank=True, null=True)
    destination_address = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route'


class RouteDiversion(models.Model):
    vehicle_id = models.IntegerField(blank=True, null=True)
    trip_id = models.IntegerField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route_diversion'


class ShipmentDetails(models.Model):
    shipment_id = models.IntegerField(blank=True, null=True)
    invoice_no = models.TextField(blank=True, null=True)
    invoice = models.BinaryField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    invoice_value = models.TextField(blank=True, null=True)
    lr = models.BinaryField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    pod = models.BinaryField(blank=True, null=True)
    lrno = models.TextField(blank=True, null=True)
    podno = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    quantity = models.TextField(blank=True, null=True)
    ewaybillno = models.TextField(blank=True, null=True)
    final_weight = models.FloatField(blank=True, null=True)
    drop_id = models.IntegerField(blank=True, null=True)
    consignment_id = models.TextField(blank=True, null=True)
    customer_lr_number = models.TextField(blank=True, null=True)
    customer_pod_number = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    freight_payment_term = models.TextField(blank=True, null=True)
    freight_charge = models.FloatField(blank=True, null=True)
    sur_charge = models.FloatField(blank=True, null=True)
    cover_charges_or_cr = models.FloatField(blank=True, null=True)
    cover_collection_charge = models.FloatField(blank=True, null=True)
    door_collection_charge = models.FloatField(blank=True, null=True)
    door_delivery_charge = models.FloatField(blank=True, null=True)
    value_added_service_charge = models.FloatField(blank=True, null=True)
    statistical_charge = models.FloatField(blank=True, null=True)
    handling_charges = models.FloatField(blank=True, null=True)
    insurance_amount = models.FloatField(blank=True, null=True)
    insurance_company = models.TextField(blank=True, null=True)
    policy_no = models.TextField(blank=True, null=True)
    consignor_description = models.TextField(blank=True, null=True)
    consignor_remark = models.TextField(blank=True, null=True)
    booking_employee_name = models.TextField(blank=True, null=True)
    consignor_signature = models.TextField(blank=True, null=True)
    policy_date = models.DateTimeField(blank=True, null=True)
    eway_bill_file = models.BinaryField(blank=True, null=True)
    vendor_lr_file = models.BinaryField(blank=True, null=True)
    vendor_lr_number = models.TextField(blank=True, null=True)
    charged_shipment_weight = models.FloatField(blank=True, null=True)
    charged_shipment_unit = models.TextField(blank=True, null=True)
    sub_total_amount = models.FloatField(blank=True, null=True)
    igst_amount = models.FloatField(blank=True, null=True)
    sgst_amount = models.FloatField(blank=True, null=True)
    grand_total_amount = models.FloatField(blank=True, null=True)
    cgsst_amount = models.FloatField(blank=True, null=True)
    misc_charge = models.FloatField(blank=True, null=True)
    consignee_description = models.TextField(blank=True, null=True)
    customer_lr_consignor_copy_link = models.TextField(blank=True, null=True)
    customer_lr_account_copy_link = models.TextField(blank=True, null=True)
    customer_lr_branch_copy_link = models.TextField(blank=True, null=True)
    customer_pod_copy_link = models.TextField(blank=True, null=True)
    customer_lr_consignee_copy_link = models.TextField(blank=True, null=True)
    customer_lr_status = models.TextField(blank=True, null=True)
    pod_generation_datetime = models.DateTimeField(blank=True, null=True)
    lr_generation_datetime = models.DateTimeField(blank=True, null=True)
    consignee_signature = models.TextField(blank=True, null=True)
    customer_lr_numbers_id = models.IntegerField(blank=True, null=True)
    schedule_delivery_date = models.DateField(blank=True, null=True)
    vendor_lr_date = models.DateTimeField(blank=True, null=True)
    consolidated_ewaybillno = models.TextField(blank=True, null=True)
    customer_lr_consignor_consignee_copy_link = models.TextField(blank=True, null=True)
    booking_employee_id = models.TextField(blank=True, null=True)
    combined_lr_pdf_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shipment_details'


class Sos(models.Model):
    trip_id = models.IntegerField(blank=True, null=True)
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING)
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    event = models.ForeignKey(Events, models.DO_NOTHING)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sos'


class Sosvehicles(models.Model):
    userid = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    regno = models.TextField(blank=True, null=True)
    gcm = models.TextField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    location_update_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sosvehicles'


class Source(models.Model):
    company_name = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    mobile = models.TextField(blank=True, null=True)
    landline = models.TextField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    added_by = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    customeraddress_id = models.IntegerField(blank=True, null=True)
    address_name = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source'


class SubBranchLr(models.Model):
    sub_branch = models.ForeignKey('Warehouse', models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    requested_lr_number = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    total_lr_allocated = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_branch_lr'


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    subscription_short_decription = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    subscription_days = models.IntegerField(blank=True, null=True)
    subscription_freetrips = models.IntegerField(blank=True, null=True)
    subscription_freecredits = models.IntegerField(blank=True, null=True)
    subscription_cost = models.IntegerField(blank=True, null=True)
    subscription_status = models.TextField(blank=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True)
    updated_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription'


class SubscriptionTransaction(models.Model):
    subscription_transaction_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    subscription = models.ForeignKey(Subscription, models.DO_NOTHING, blank=True, null=True)
    subscription_start_date = models.DateTimeField(blank=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True)
    subscription_transaction_timestamp = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription_transaction'


class SuppRoles(models.Model):
    role_id = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    role_name = models.CharField(max_length=200)
    role_create_date = models.DateField()
    role_status = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supp_roles'


class ThcDetails(models.Model):
    thc_details_id = models.AutoField(primary_key=True)
    thc_masters = models.ForeignKey('ThcMasters', models.DO_NOTHING, blank=True, null=True)
    thc_number = models.TextField(blank=True, null=True)
    master_trip_id = models.IntegerField(blank=True, null=True)
    reference_number = models.TextField(blank=True, null=True)
    vehicle_number = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    vendor_code = models.TextField(blank=True, null=True)
    branch = models.TextField(blank=True, null=True)
    driver_name = models.TextField(blank=True, null=True)
    vehicle_type = models.TextField(blank=True, null=True)
    driver_mobile_no = models.TextField(blank=True, null=True)
    sub_branch = models.TextField(blank=True, null=True)
    total_freight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    thc_creation_date = models.DateField(blank=True, null=True)
    thc_creation_time = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    lr_no = models.TextField(blank=True, null=True)
    lr_date = models.DateField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    drop_id = models.IntegerField(blank=True, null=True)
    no_of_packages = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    actual_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    chargable_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thc_details'


class ThcMasters(models.Model):
    thc_masters_id = models.AutoField(primary_key=True)
    thc_number = models.TextField(blank=True, null=True)
    master_trip_id = models.IntegerField(blank=True, null=True)
    reference_number = models.TextField(blank=True, null=True)
    vehicle_number = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    vendor_code = models.TextField(blank=True, null=True)
    payment_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    approval_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    rejection_reason = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    branch_code_sequence = models.IntegerField(blank=True, null=True)
    raised_by_id = models.IntegerField(blank=True, null=True)
    checked_by_id = models.IntegerField(blank=True, null=True)
    approved_by_id = models.IntegerField(blank=True, null=True)
    branch_code = models.IntegerField(blank=True, null=True)
    thc_report_link = models.TextField(blank=True, null=True)
    thc_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thc_masters'


class ThcNumberFormat(models.Model):
    thc_format_id = models.AutoField(primary_key=True)
    thc_format = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thc_number_format'


class ThcPaymentCharges(models.Model):
    thc_charges_id = models.AutoField(primary_key=True)
    thc_payment = models.ForeignKey('ThcPayments', models.DO_NOTHING, blank=True, null=True)
    advance = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    advance_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    loading_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    halting_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    unloading_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    police_rto = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    misc_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cgst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    igst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tds = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_freight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    final_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    thc_masters_id = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    advance_check_no = models.TextField(blank=True, null=True)
    account_number = models.TextField(blank=True, null=True)
    ifsc_code = models.TextField(blank=True, null=True)
    misc_desc = models.TextField(blank=True, null=True)
    total_tax = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    final_check_no = models.TextField(blank=True, null=True)
    advance_check_date = models.DateField(blank=True, null=True)
    final_check_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thc_payment_charges'


class ThcPayments(models.Model):
    thc_payment_id = models.AutoField(primary_key=True)
    thc_masters = models.ForeignKey(ThcMasters, models.DO_NOTHING, blank=True, null=True)
    payment_type = models.TextField(blank=True, null=True)
    payment_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thc_payments'


class TransactionEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction_event'


class TransoCreditTransaction(models.Model):
    transo_credit_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)
    transaction_event = models.ForeignKey(TransactionEvent, models.DO_NOTHING, blank=True, null=True)
    transaction_timestamp = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transo_credit_transaction'


class TransoMoneyTransaction(models.Model):
    transo_money_transaction_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)
    transaction_event_id = models.IntegerField(blank=True, null=True)
    transaction_timestamp = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transo_money_transaction'


class Trip(models.Model):
    shipment_id = models.TextField(blank=True, null=True)
    vehicle_booking_details = models.ForeignKey('VehicleBookingDetails', models.DO_NOTHING, db_column='vehicle_booking_details')
    trip_km = models.FloatField(blank=True, null=True)
    actual_eta = models.DateTimeField(blank=True, null=True)
    trip_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    time_stamp = models.DateTimeField(blank=True, null=True)
    rem_distance = models.TextField(blank=True, null=True)
    driver_status = models.TextField(blank=True, null=True)
    reason_toend = models.TextField(blank=True, null=True)
    free_trip = models.BooleanField(blank=True, null=True)
    pickup_km = models.FloatField(blank=True, null=True)
    driver_notification_status = models.TextField()
    trip_ended_lattitude = models.FloatField(blank=True, null=True)
    trip_ended_longitute = models.FloatField(blank=True, null=True)
    driver_status_updated_on = models.DateTimeField(blank=True, null=True)
    driver_final_trip_status = models.TextField(blank=True, null=True)
    driver_auto_reject = models.BooleanField(blank=True, null=True)
    actual_distance = models.FloatField(blank=True, null=True)
    current_eta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip'


class TripClosureRemark(models.Model):
    remark = models.TextField(blank=True, null=True)
    remark_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_closure_remark'


class TripConsignment(models.Model):
    vehicle_booking_details = models.ForeignKey('VehicleBookingDetails', models.DO_NOTHING, blank=True, null=True)
    drop = models.ForeignKey(Drops, models.DO_NOTHING, blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    trip_km = models.FloatField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    material_type = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    material_quantity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    drop_status = models.CharField(max_length=255, blank=True, null=True)
    rem_distance = models.TextField(blank=True, null=True)
    driver_status = models.TextField(blank=True, null=True)
    reason_toend = models.TextField(blank=True, null=True)
    pickup_km = models.FloatField(blank=True, null=True)
    trip_ended_lattitude = models.FloatField(blank=True, null=True)
    trip_ended_longitute = models.FloatField(blank=True, null=True)
    driver_status_updated_on = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    loading = models.TextField(blank=True, null=True)
    unloading = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    payment_mode = models.CharField(max_length=100, blank=True, null=True)
    length = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    breadth = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    trip_consignment_id = models.AutoField(primary_key=True)
    payment_id = models.CharField(max_length=-1, blank=True, null=True)
    payment_otp = models.IntegerField(blank=True, null=True)
    payment_status = models.TextField(blank=True, null=True)
    consignment_id = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    drop_route_sequence = models.IntegerField(blank=True, null=True)
    material_type_0 = models.ForeignKey(MaterialType, models.DO_NOTHING, db_column='material_type_id', blank=True, null=True)  # Field renamed because of name conflict.
    customer_lr_number = models.TextField(blank=True, null=True)
    customer_lr_numbers_id = models.IntegerField(blank=True, null=True)
    road_distance = models.TextField(blank=True, null=True)
    master_vehicle_type = models.TextField(blank=True, null=True)
    master_tat = models.TextField(blank=True, null=True)
    master_distance = models.TextField(blank=True, null=True)
    master_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shipment_load = models.TextField(blank=True, null=True)  # This field type is a guess.
    load_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    material_description = models.TextField(blank=True, null=True)
    actual_eta = models.DateTimeField(blank=True, null=True)
    actual_distance = models.FloatField(blank=True, null=True)
    actual_dispatch_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_consignment'


class TripConsignmentPackageDetails(models.Model):
    trip_consignment = models.ForeignKey(TripConsignment, models.DO_NOTHING, blank=True, null=True)
    no_of_box = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    breadth = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    volume_of_cargo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    carrier_volumetric_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    customer_volumetric_weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_consignment_package_details'


class TripDocumentType(models.Model):
    trip_document_type_id = models.AutoField(primary_key=True)
    type = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_document_type'


class TripDocuments(models.Model):
    trip_documents_id = models.AutoField(primary_key=True)
    document_type = models.TextField(blank=True, null=True)
    document_number = models.TextField(blank=True, null=True)
    document_image = models.BinaryField(blank=True, null=True)
    document_barcode = models.BinaryField(blank=True, null=True)
    added_by_company_id = models.IntegerField(blank=True, null=True)
    added_by_user_id = models.IntegerField(blank=True, null=True)
    added_by_driver_id = models.IntegerField(blank=True, null=True)
    added_on_datetime = models.DateTimeField(blank=True, null=True)
    trip = models.ForeignKey(Trip, models.DO_NOTHING, blank=True, null=True)
    master_trip = models.ForeignKey(MasterTrip, models.DO_NOTHING, blank=True, null=True)
    trip_consignment = models.ForeignKey(TripConsignment, models.DO_NOTHING, blank=True, null=True)
    document_datetime = models.DateTimeField(blank=True, null=True)
    trip_document_type = models.ForeignKey(TripDocumentType, models.DO_NOTHING, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    valid_upto = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    document_value = models.TextField(blank=True, null=True)
    consolidate_ewaybill_no = models.TextField(blank=True, null=True)
    document_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_documents'


class TripEmails(models.Model):
    trip_email_id = models.AutoField(primary_key=True)
    email_status = models.TextField(blank=True, null=True)
    user_email_id = models.TextField(blank=True, null=True)
    consignor_email_id = models.TextField(blank=True, null=True)
    consignee_email_id = models.TextField(blank=True, null=True)
    email_recipient_role = models.TextField(blank=True, null=True)
    email_subject = models.TextField(blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    master_trip_id = models.IntegerField(blank=True, null=True)
    trip_id = models.IntegerField(blank=True, null=True)
    drop_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_emails'


class TripEvents(models.Model):
    trip = models.ForeignKey(Trip, models.DO_NOTHING)
    event = models.ForeignKey(Events, models.DO_NOTHING)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_events'


class TripRoute(models.Model):
    trip = models.ForeignKey(Trip, models.DO_NOTHING, blank=True, null=True)
    route = models.ForeignKey(Route, models.DO_NOTHING, blank=True, null=True)
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_route'


class TripTrack(models.Model):
    master_trip = models.ForeignKey(MasterTrip, models.DO_NOTHING)
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING)
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    trip = models.ForeignKey(Trip, models.DO_NOTHING)
    drop = models.ForeignKey(Drops, models.DO_NOTHING)
    status = models.TextField(blank=True, null=True)
    trip_end_reason = models.TextField(blank=True, null=True)
    round_trip_id = models.IntegerField(blank=True, null=True)
    trip_close = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_track'


class UserRoles(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    username = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    user_id = models.IntegerField()
    roles = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_roles'


class UserRolesBak16Sep2020(models.Model):
    user_role_id = models.IntegerField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    roles = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_roles_bak_16sep2020'


class Userdocuments(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    documentid = models.ForeignKey(Documenttype, models.DO_NOTHING, db_column='documentid')
    document = models.BinaryField(blank=True, null=True)
    verified = models.TextField(blank=True, null=True)  # This field type is a guess.
    verification_reason = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userdocuments'


class Users(models.Model):
    emailid = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    authorisation_status = models.BooleanField(blank=True, null=True)
    dob = models.CharField(max_length=100, blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    profilepic = models.BinaryField(blank=True, null=True)
    phone_mobile = models.TextField(blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    company_id = models.AutoField()
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)
    gcm_token = models.CharField(max_length=-1, blank=True, null=True)
    eway_bill_auth_token = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    user_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    imei = models.CharField(max_length=200, blank=True, null=True)
    otp = models.CharField(max_length=15, blank=True, null=True)
    otp_gen_time = models.DateTimeField(blank=True, null=True)
    otp_exp_time = models.DateTimeField(blank=True, null=True)
    employee_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('emailid', 'phone_mobile', 'username'),)


class UsersBak16Sep2020(models.Model):
    id = models.IntegerField(blank=True, null=True)
    emailid = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    authorisation_status = models.BooleanField(blank=True, null=True)
    dob = models.CharField(max_length=100, blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    profilepic = models.BinaryField(blank=True, null=True)
    phone_mobile = models.TextField(blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    gcm_token = models.CharField(max_length=-1, blank=True, null=True)
    eway_bill_auth_token = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    user_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    imei = models.CharField(max_length=200, blank=True, null=True)
    otp = models.CharField(max_length=15, blank=True, null=True)
    otp_gen_time = models.DateTimeField(blank=True, null=True)
    otp_exp_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_bak_16sep2020'


class UsersBranchRelationship(models.Model):
    branch_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_branch_relationship'


class Vehicle(models.Model):
    regno = models.TextField(blank=True, null=True)
    company_id = models.AutoField()
    engineno = models.TextField(blank=True, null=True)
    chassisno = models.TextField(blank=True, null=True)
    registeredstate = models.TextField(blank=True, null=True)
    registereddate = models.DateField(blank=True, null=True)
    registeredauthority = models.TextField(blank=True, null=True)
    parentage = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    gcm_token = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    driver = models.ForeignKey(Driver, models.DO_NOTHING, blank=True, null=True)
    manufacturedate = models.TextField(blank=True, null=True)
    app_version = models.FloatField(blank=True, null=True)
    verification_status = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    permit_type_id = models.IntegerField(blank=True, null=True)
    contract_type_id = models.IntegerField(blank=True, null=True)
    ltl_vehicle = models.BooleanField(blank=True, null=True)
    ltl_vehicle_sequence = models.IntegerField(blank=True, null=True)
    driver_app_status = models.BooleanField(blank=True, null=True)
    gps_device_id = models.TextField(blank=True, null=True)
    gps = models.BooleanField(blank=True, null=True)
    mobile = models.BooleanField(blank=True, null=True)
    gps_device_provider = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle'


class VehicleAttr(models.Model):
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)
    vehicle_type_id = models.IntegerField(blank=True, null=True)
    cap_ton = models.FloatField(blank=True, null=True)
    volume_cm = models.FloatField(blank=True, null=True)
    volume_ltrs = models.FloatField(blank=True, null=True)
    length_m = models.FloatField(blank=True, null=True)
    height_m = models.FloatField(blank=True, null=True)
    width_m = models.FloatField(blank=True, null=True)
    class_field = models.TextField(db_column='class', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    model = models.TextField(blank=True, null=True)
    sub_model = models.TextField(blank=True, null=True)
    manufacturer_name = models.TextField(blank=True, null=True)
    odometer = models.FloatField(blank=True, null=True)
    fuel_capacity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    capacity_kg = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_attr'


class VehicleBookingDetails(models.Model):
    booking = models.ForeignKey(Booking, models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)
    vehicle_type = models.TextField(blank=True, null=True)
    vehicle_company_id = models.IntegerField()
    time_stamp = models.DateTimeField(blank=True, null=True)
    rejected_by = models.IntegerField(blank=True, null=True)
    shipper_quote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carrier_quote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    remaining_weight = models.FloatField(blank=True, null=True)
    next_booking = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    other_rejection_reason = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'vehicle_booking_details'


class VehicleBookingDetailsOld(models.Model):
    booking = models.ForeignKey(BookingOld, models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)
    vehicle_type = models.TextField(blank=True, null=True)
    vehicle_company_id = models.AutoField()
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    time_stamp = models.DateTimeField(blank=True, null=True)
    rejected_by = models.IntegerField(blank=True, null=True)
    shipper_quote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carrier_quote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rejected_date = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    other_rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_booking_details_old'


class VehicleBookingDetailsold(models.Model):
    id = models.IntegerField(blank=True, null=True)
    booking_id = models.IntegerField(blank=True, null=True)
    vehicle_id = models.IntegerField(blank=True, null=True)
    vehicle_type = models.TextField(blank=True, null=True)
    vehicle_company_id = models.IntegerField(blank=True, null=True)
    shipper_quote = models.TextField(blank=True, null=True)
    carrier_quote = models.TextField(blank=True, null=True)
    final_price = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    time_stamp = models.DateTimeField(blank=True, null=True)
    rejected_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_booking_detailsold'


class VehicleClass(models.Model):
    class_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_class'


class VehicleDestination(models.Model):
    geofence_location = models.ForeignKey(GeofenceLocation, models.DO_NOTHING, blank=True, null=True)
    location_type = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    contact_mobile_number = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    contact_email_id = models.TextField(blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    material_id = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    charged_weight = models.IntegerField(blank=True, null=True)
    radius = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_destination'


class VehicleJrmRoute(models.Model):
    id = models.IntegerField(primary_key=True)
    vehicle_id = models.IntegerField()
    jrm_route_id = models.IntegerField()
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_jrm_route'


class VehicleRoute(models.Model):
    route = models.ForeignKey(Route, models.DO_NOTHING, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_route'


class VehicleSource(models.Model):
    geofence_location = models.ForeignKey(GeofenceLocation, models.DO_NOTHING, blank=True, null=True)
    location_type = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    contact_mobile_number = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    contact_email_id = models.TextField(blank=True, null=True)
    radius = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_source'


class VehicleStatus(models.Model):
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)
    company_id = models.AutoField()
    regno = models.TextField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    trip_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    location_update_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    lasttripdate = models.DateField(blank=True, null=True)
    vehicle_status = models.TextField(blank=True, null=True)
    odometer = models.FloatField(blank=True, null=True)
    locker_id = models.TextField(blank=True, null=True)
    locker_number = models.TextField(blank=True, null=True)
    battery_strength = models.FloatField(blank=True, null=True)
    signal_strength = models.FloatField(blank=True, null=True)
    gps_status = models.TextField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    status_updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_status'


class VehicleStoppage(models.Model):
    vehicle_id = models.IntegerField()
    start_latitude = models.FloatField(blank=True, null=True)
    start_longitude = models.FloatField(blank=True, null=True)
    end_latitude = models.FloatField(blank=True, null=True)
    end_longitude = models.FloatField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_stoppage'


class VehicleSubModel(models.Model):
    sub_model_name = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    manufacture_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_sub_model'


class VehicleSubscription(models.Model):
    vehicle_subscription_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, blank=True, null=True)
    vehicle_start_date = models.DateTimeField(blank=True, null=True)
    vehicle_end_date = models.DateTimeField(blank=True, null=True)
    subscription_status = models.TextField(blank=True, null=True)
    subscription_freetrips_remaining = models.IntegerField(blank=True, null=True)
    updated_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_subscription'


class VehicleTemp(models.Model):
    id = models.BigAutoField(primary_key=True)
    regno = models.TextField(blank=True, null=True)
    company_id = models.IntegerField()
    engineno = models.TextField(blank=True, null=True)
    chassisno = models.TextField(blank=True, null=True)
    registeredstate = models.TextField(blank=True, null=True)
    registereddate = models.DateField(blank=True, null=True)
    registeredauthority = models.TextField(blank=True, null=True)
    manufacturedate = models.TextField(blank=True, null=True)
    vehicle_type_id = models.IntegerField(blank=True, null=True)
    cap_ton = models.FloatField(blank=True, null=True)
    volume_cm = models.FloatField(blank=True, null=True)
    volume_ltrs = models.FloatField(blank=True, null=True)
    length_m = models.FloatField(blank=True, null=True)
    height_m = models.FloatField(blank=True, null=True)
    width_m = models.FloatField(blank=True, null=True)
    class_field = models.TextField(db_column='class', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    model = models.TextField(blank=True, null=True)
    sub_model = models.TextField(blank=True, null=True)
    manufacturer_name = models.TextField(blank=True, null=True)
    odometer = models.FloatField(blank=True, null=True)
    fuel_capacity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    permit_type_id = models.IntegerField(blank=True, null=True)
    contract_type_id = models.IntegerField(blank=True, null=True)
    ltl_vehicle = models.BooleanField(blank=True, null=True)
    ltl_vehicle_sequence = models.IntegerField(blank=True, null=True)
    driver_app_status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_temp'


class VehicleType(models.Model):
    type = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    max_ton_capacity = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_type'


class VehicleViolations(models.Model):
    vehicle_id = models.IntegerField(blank=True, null=True)
    event_type = models.TextField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    trip_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_violations'
        unique_together = (('vehicle_id', 'event_type', 'event_time'),)


class Vehicledocumentlist(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicledocumentlist'


class Vehicledocuments(models.Model):
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)
    document = models.BinaryField(blank=True, null=True)
    verified = models.TextField(blank=True, null=True)  # This field type is a guess.
    verification_reason = models.TextField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    documentid = models.ForeignKey(Vehicledocumentlist, models.DO_NOTHING, db_column='documentid', blank=True, null=True)
    updated_status = models.BooleanField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicledocuments'


class Vendor(models.Model):
    vendor_name = models.TextField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    pan_number = models.TextField(blank=True, null=True)
    gst_number = models.TextField(blank=True, null=True)
    cin_number = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    email_id = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING)
    time_stamp = models.DateTimeField(blank=True, null=True)
    vendor_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'vendor'


class VendorContractRouteRate(models.Model):
    vendor_id = models.IntegerField(blank=True, null=True)
    source_state = models.TextField(blank=True, null=True)
    destination_state = models.TextField(blank=True, null=True)
    source_city = models.TextField(blank=True, null=True)
    destination_city = models.TextField(blank=True, null=True)
    rate = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor_contract_route_rate'


class VendorDriver(models.Model):
    driver = models.ForeignKey(Driver, models.DO_NOTHING, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor_driver'


class VendorVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor_vehicle'


class Videoupload(models.Model):
    cid = models.IntegerField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    regno = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    recorded_time = models.DateTimeField(blank=True, null=True)
    data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'videoupload'


class Warehouse(models.Model):
    warehouse_name = models.TextField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    warehouse_location = models.TextField(blank=True, null=True)
    warehouse_latitude = models.FloatField(blank=True, null=True)
    warehouse_longitude = models.FloatField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    google_address = models.TextField(blank=True, null=True)
    address_line_one = models.TextField(blank=True, null=True)
    address_line_two = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouse'

