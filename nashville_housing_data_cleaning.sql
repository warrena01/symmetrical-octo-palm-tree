
-- First look at the data: general look, uniformity in typically problematic columns, usability of data
select * 
from nashville_data_cleaning..NashvilleHousing

select SoldAsVacant, count(SoldAsVacant) as 'count'
from nashville_data_cleaning..NashvilleHousing
group by SoldAsVacant


/* Problems Identified:
- SaleDate isnt in a neat format
- PropertyAddress has null fields
- PropertyAddress and OwnerAddress format isnt very usable
- SoldAsVacant has N, Yes, Y, No columns */


-- Standardizing Date Format (Two Methods)


select SaleDate, format(SaleDateStandardized, 'dd-MM-yyyy') as SaleDateStandardized
from nashville_data_cleaning..NashvilleHousing

select format(SaleDate, 'dd-MM-yyyy') -- this works to format an answer but not to update tables
from nashville_data_cleaning..NashvilleHousing

select convert(date, SaleDate)
from nashville_data_cleaning..NashvilleHousing 

update NashvilleHousing -- this isnt working, as such will use alter table and then update
set SaleDate = convert(date, SaleDate)

alter table NashvilleHousing
add SaleDateStandardized Date

update NashvilleHousing
set SaleDateStandardized = convert(Date,SaleDate)


-- Populating Null PropertyAddress


Select ParcelID,PropertyAddress, OwnerAddress -- PropertyAddress is null when there is a preceeding row with the same ParcelID
From nashville_data_cleaning..NashvilleHousing
-- where PropertyAddress is null (check at the end)
order by ParcelID

select  a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, 
		isnull(a.PropertyAddress, b.PropertyAddress)
from nashville_data_cleaning..NashvilleHousing a
join nashville_data_cleaning..NashvilleHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] != b.[UniqueID ]
where a.PropertyAddress is null

update a 
set PropertyAddress = isnull(a.PropertyAddress, b.PropertyAddress)
from nashville_data_cleaning..NashvilleHousing a
join nashville_data_cleaning..NashvilleHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] != b.[UniqueID ]
where a.PropertyAddress is null


-- Seperate PropertyAddress Columns Method 1

select  PropertyAddress,
		substring(PropertyAddress, 1, charindex(',', PropertyAddress) -1) as Address, -- (-1) stops before the first instance of ','
		substring(PropertyAddress, charindex(',', PropertyAddress) +1, len(PropertyAddress)) as District
from nashville_data_cleaning..NashvilleHousing

alter table NashvilleHousing
add PropertyAddressStreet nvarchar(255)
update NashvilleHousing
set PropertyAddressStreet = substring(PropertyAddress, 1, charindex(',', PropertyAddress) -1) 

alter table NashvilleHousing
add PropertyAddressDistrict nvarchar(255)
update NashvilleHousing
set PropertyAddressDistrict = substring(PropertyAddress, charindex(',', PropertyAddress) +1, len(PropertyAddress))

select * from nashville_data_cleaning..NashvilleHousing

-- Seperate OwnerAddress Columns Method 2

select  OwnerAddress,
		parsename(replace(OwnerAddress, ',', '.'), 3) as OwnerAddressStreet,
		parsename(replace(OwnerAddress, ',', '.'), 2) as OwnerAddressDistrict,
		parsename(replace(OwnerAddress, ',', '.'), 1) as OwnerAddressState
from nashville_data_cleaning..NashvilleHousing

alter table NashvilleHousing
add OwnerAddressStreet nvarchar(255)
alter table NashvilleHousing
add OwnerAddressDistrict nvarchar(255)
alter table NashvilleHousing
add OwnerAddressState nvarchar(255)

update NashvilleHousing
set OwnerAddressStreet = parsename(replace(OwnerAddress, ',', '.'), 3) 
update NashvilleHousing
set OwnerAddressDistrict = parsename(replace(OwnerAddress, ',', '.'), 2)
update NashvilleHousing
set OwnerAddressState = parsename(replace(OwnerAddress, ',', '.'), 1)


-- Standardize Responses for Y,Yes,No,N

with cte as (
Select SoldAsVacant
, CASE When SoldAsVacant = 'Y' THEN 'Yes'
	   When SoldAsVacant = 'N' THEN 'No'
	   ELSE SoldAsVacant
	   END as 'organized'
From nashville_data_cleaning..NashvilleHousing)
select count(distinct(organized))
from cte

update NashvilleHousing
set  SoldAsVacant = CASE When SoldAsVacant = 'Y' THEN 'Yes'
	   When SoldAsVacant = 'N' THEN 'No'
	   ELSE SoldAsVacant
	   END

select  count(distinct(SoldAsVacant))
from nashville_data_cleaning..NashvilleHousing


-- Remove Duplicates

with row_num_cte as (
select  *,
		row_number() over (
		partition by ParcelId, PropertyAddress, SalePrice, SaleDate, LegalReference
		order by ParcelId) as row_num
from nashville_data_cleaning..NashvilleHousing)
delete
from row_num_cte
where row_num > 1

with row_num_cte as ( -- check that it worked
select  *,
		row_number() over (
		partition by ParcelId, PropertyAddress, SalePrice, SaleDate, LegalReference
		order by ParcelId) as row_num
from nashville_data_cleaning..NashvilleHousing)
select *
from row_num_cte
where row_num > 1


-- Remove Unusable Columns

alter table NashvilleHousing
drop column OwnerAddress, PropertyAddress, SaleDate




